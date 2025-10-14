"""
Обработчики для работы с напоминаниями
"""
import logging
import aiohttp
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from datetime import datetime, timedelta
import os

logger = logging.getLogger(__name__)
router = Router()

API_URL = os.getenv('API_URL', 'http://localhost:8000')

class ReminderStates(StatesGroup):
    waiting_for_event_name = State()
    waiting_for_event_date = State()
    waiting_for_remind_days = State()

async def get_user_reminders(telegram_id: int):
    """Получить напоминания пользователя из API"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_URL}/api/reminders/{telegram_id}") as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"Ошибка получения напоминаний: {response.status}")
                    return []
    except Exception as e:
        logger.error(f"Ошибка API запроса: {e}")
        return []

async def create_reminder(telegram_id: int, event_name: str, event_date: str, remind_days: int):
    """Создать напоминание через API"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{API_URL}/api/reminders", json={
                "telegram_id": telegram_id,
                "event_name": event_name,
                "event_date": event_date,
                "remind_days_before": remind_days
            }) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"Ошибка создания напоминания: {response.status}")
                    return None
    except Exception as e:
        logger.error(f"Ошибка API запроса: {e}")
        return None

@router.message(F.text == "🔔 Напоминания")
async def reminders_menu(message: Message):
    """Меню напоминаний"""
    logger.info(f"🔔 Запрос напоминаний от {message.from_user.id}")
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Добавить напоминание", callback_data="add_reminder")],
        [InlineKeyboardButton(text="📝 Мои напоминания", callback_data="list_reminders")]
    ])
    
    await message.answer(
        "🔔 <b>Напоминания о важных датах</b>\n\n"
        "Не забудьте о днях рождения, годовщинах и других важных событиях!\n"
        "Мы напомним вам заранее, чтобы вы успели заказать букет.",
        reply_markup=keyboard,
        parse_mode='HTML'
    )

@router.callback_query(F.data == "add_reminder")
async def add_reminder_start(callback_query: CallbackQuery, state: FSMContext):
    """Начать процесс добавления напоминания"""
    await state.set_state(ReminderStates.waiting_for_event_name)
    
    await callback_query.message.edit_text(
        "➕ <b>Добавить напоминание</b>\n\n"
        "📝 Введите название события:\n"
        "Например: День рождения мамы, Годовщина свадьбы, 8 марта",
        parse_mode='HTML'
    )
    
    await callback_query.answer()

@router.message(ReminderStates.waiting_for_event_name)
async def process_event_name(message: Message, state: FSMContext):
    """Обработать название события"""
    event_name = message.text.strip()
    
    if len(event_name) < 3:
        await message.answer("❌ Название события слишком короткое. Попробуйте еще раз:")
        return
    
    await state.update_data(event_name=event_name)
    await state.set_state(ReminderStates.waiting_for_event_date)
    
    await message.answer(
        f"📅 <b>Дата события</b>\n\n"
        f"Событие: {event_name}\n\n"
        f"Введите дату в формате ДД.ММ.ГГГГ:\n"
        f"Например: 15.03.2025",
        parse_mode='HTML'
    )

@router.message(ReminderStates.waiting_for_event_date)
async def process_event_date(message: Message, state: FSMContext):
    """Обработать дату события"""
    date_text = message.text.strip()
    
    try:
        # Парсим дату
        day, month, year = date_text.split('.')
        event_date = datetime(int(year), int(month), int(day))
        
        # Проверяем что дата в будущем
        if event_date <= datetime.now():
            await message.answer("❌ Дата должна быть в будущем. Попробуйте еще раз:")
            return
            
    except ValueError:
        await message.answer("❌ Неверный формат даты. Используйте ДД.ММ.ГГГГ:")
        return
    
    await state.update_data(event_date=date_text)
    await state.set_state(ReminderStates.waiting_for_remind_days)
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="1 день", callback_data="remind_1")],
        [InlineKeyboardButton(text="3 дня", callback_data="remind_3")],
        [InlineKeyboardButton(text="7 дней", callback_data="remind_7")],
        [InlineKeyboardButton(text="14 дней", callback_data="remind_14")]
    ])
    
    await message.answer(
        f"⏰ <b>За сколько дней напомнить?</b>\n\n"
        f"Событие: {event_date.strftime('%d.%m.%Y')}\n"
        f"Выберите когда напомнить:",
        reply_markup=keyboard,
        parse_mode='HTML'
    )

@router.callback_query(F.data.startswith("remind_"))
async def process_remind_days(callback_query: CallbackQuery, state: FSMContext):
    """Обработать выбор дней для напоминания"""
    remind_days = int(callback_query.data.replace("remind_", ""))
    
    data = await state.get_data()
    event_name = data['event_name']
    event_date = data['event_date']
    
    # Создаем напоминание
    result = await create_reminder(
        callback_query.from_user.id,
        event_name,
        event_date,
        remind_days
    )
    
    if result:
        await callback_query.message.edit_text(
            f"✅ <b>Напоминание добавлено!</b>\n\n"
            f"📝 Событие: {event_name}\n"
            f"📅 Дата: {event_date}\n"
            f"⏰ Напомним за {remind_days} дней\n\n"
            f"Мы напомним вам заранее, чтобы вы успели заказать букет!",
            parse_mode='HTML'
        )
    else:
        await callback_query.message.edit_text(
            "❌ <b>Ошибка</b>\n\n"
            "Не удалось добавить напоминание. Попробуйте позже.",
            parse_mode='HTML'
        )
    
    await state.clear()
    await callback_query.answer()

@router.callback_query(F.data == "list_reminders")
async def list_reminders(callback_query: CallbackQuery):
    """Показать список напоминаний"""
    reminders = await get_user_reminders(callback_query.from_user.id)
    
    if not reminders:
        await callback_query.message.edit_text(
            "📝 <b>Мои напоминания</b>\n\n"
            "У вас пока нет напоминаний.\n"
            "Добавьте первое напоминание!",
            parse_mode='HTML'
        )
        await callback_query.answer()
        return
    
    text = "📝 <b>Мои напоминания:</b>\n\n"
    
    for reminder in reminders:
        text += f"📅 <b>{reminder['event_name']}</b>\n"
        text += f"Дата: {reminder['event_date']}\n"
        text += f"Напомнить за: {reminder['remind_days_before']} дней\n\n"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Добавить еще", callback_data="add_reminder")]
    ])
    
    await callback_query.message.edit_text(
        text,
        reply_markup=keyboard,
        parse_mode='HTML'
    )
    
    await callback_query.answer()

