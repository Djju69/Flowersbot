"""
Обработчики команд бота - точно по ТЗ
"""
import logging
from aiogram.types import Message, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import os

logger = logging.getLogger(__name__)

WEBAPP_URL = os.getenv('WEBAPP_URL', 'https://flowersbot-production.up.railway.app/webapp')

async def cmd_start(message: Message):
    """Команда /start - точно по ТЗ"""
    logger.info(f"🎯 Получена команда /start от пользователя {message.from_user.id}")
    
    # Reply keyboard с кнопками по ТЗ
    reply_kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="🛍 Магазин"), KeyboardButton(text="🔁 Повторить")],
        [KeyboardButton(text="📦 Мои заказы"), KeyboardButton(text="💬 Поддержка")]
    ], resize_keyboard=True)
    
    # Приветственное сообщение
    await message.answer(
        "🌸 <b>Добро пожаловать в Цветы Нячанг!</b>\n\n"
        "Свежие букеты с доставкой за 1-2 часа 🚚\n"
        "📸 Фото перед отправкой\n"
        "💳 Удобная оплата\n\n"
        "Выберите действие:",
        reply_markup=reply_kb,
        parse_mode='HTML'
    )
    
    # Inline кнопка для Mini App
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🛍 ОТКРЫТЬ МАГАЗИН",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )]
    ])
    
    await message.answer(
        "🛍 Открыть магазин:",
        reply_markup=keyboard
    )

async def shop_button(message: Message):
    """Кнопка 🛍 Магазин - открывает Mini App"""
    logger.info(f"🛍 Открытие магазина от {message.from_user.id}")
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🛍 ОТКРЫТЬ МАГАЗИН",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )]
    ])
    
    await message.answer(
        "🌸 Выберите букеты:",
        reply_markup=keyboard
    )

async def repeat_button(message: Message):
    """Кнопка 🔁 Повторить - показывает последний заказ"""
    logger.info(f"🔁 Запрос повтора заказа от {message.from_user.id}")
    
    # TODO: Получить последний заказ из API
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🛍 Повторить заказ #123",
            web_app=WebAppInfo(url=f"{WEBAPP_URL}?repeat=123")
        )]
    ])
    
    await message.answer(
        "🔁 <b>Повторить последний заказ</b>\n\n"
        "📦 Заказ #123\n"
        "🌹 Розы премиум\n"
        "💰 1,200,000 VND\n\n"
        "Нажмите кнопку чтобы повторить:",
        reply_markup=keyboard,
        parse_mode='HTML'
    )

async def orders_button(message: Message):
    """Кнопка 📦 Мои заказы - история заказов"""
    logger.info(f"📦 Запрос истории заказов от {message.from_user.id}")
    
    # TODO: Получить заказы из API
    await message.answer(
        "📦 <b>Ваши заказы:</b>\n\n"
        "📦 Заказ #123\n"
        "💰 1,200,000 VND\n"
        "📅 15.10.2025\n"
        "Статус: Доставлен\n\n"
        "📦 Заказ #122\n"
        "💰 800,000 VND\n"
        "📅 10.10.2025\n"
        "Статус: Доставлен",
        parse_mode='HTML'
    )

async def support_button(message: Message):
    """Кнопка 💬 Поддержка - контактная информация"""
    logger.info(f"💬 Запрос поддержки от {message.from_user.id}")
    
    await message.answer(
        "💬 <b>Поддержка клиентов</b>\n\n"
        "📞 Телефон: +84 XXX XXX XXX\n"
        "📧 Email: support@flowers-nhatrang.com\n"
        "🕐 Время работы: 8:00 - 22:00\n\n"
        "Или напишите ваш вопрос, и мы ответим в течение 15 минут!",
        parse_mode='HTML'
    )
