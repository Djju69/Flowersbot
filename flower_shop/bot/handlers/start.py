"""
Обработчики команд старта и основных функций бота
"""
import logging
from aiogram import Router, F
from aiogram.types import Message, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart, Command
import os

logger = logging.getLogger(__name__)
router = Router()

WEBAPP_URL = os.getenv('WEBAPP_URL', 'https://flowersbot-production.up.railway.app/webapp')

@router.message(CommandStart())
async def cmd_start(message: Message):
    """Приветствие + кнопка Mini App"""
    
    logger.info(f"🎯 Получена команда /start от пользователя {message.from_user.id}")
    
    # Inline кнопка с Mini App
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🛍 ОТКРЫТЬ МАГАЗИН",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )]
    ])
    
    # Reply-кнопки для дополнительных функций
    reply_kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="🛍 Магазин"), KeyboardButton(text="🔁 Повторить")],
        [KeyboardButton(text="📦 Мои заказы"), KeyboardButton(text="💬 Поддержка")]
    ], resize_keyboard=True)
    
    await message.answer(
        "🌸 <b>Добро пожаловать в Цветы Нячанг!</b>\n\n"
        "Свежие букеты с доставкой за 1-2 часа 🚚\n"
        "📸 Фото перед отправкой\n"
        "💳 Удобная оплата\n\n"
        "Нажмите кнопку чтобы выбрать букеты:",
        reply_markup=reply_kb,
        parse_mode='HTML'
    )
    
    # Отправляем отдельно inline кнопку
    await message.answer(
        "🛍 Открыть магазин:",
        reply_markup=keyboard
    )

@router.message(F.text == "🛍 Магазин")
async def open_shop_button(message: Message):
    """Открыть магазин по кнопке"""
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

@router.message(F.text == "🔁 Повторить")
async def repeat_last_order(message: Message):
    """Повторить последний заказ"""
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

@router.message(F.text == "📦 Мои заказы")
async def my_orders(message: Message):
    """История заказов пользователя"""
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

@router.message(F.text == "💬 Поддержка")
async def support(message: Message):
    """Поддержка клиентов"""
    logger.info(f"💬 Запрос поддержки от {message.from_user.id}")
    
    await message.answer(
        "💬 <b>Поддержка клиентов</b>\n\n"
        "📞 Телефон: +84 XXX XXX XXX\n"
        "📧 Email: support@flowers-nhatrang.com\n"
        "🕐 Время работы: 8:00 - 22:00\n\n"
        "Или напишите ваш вопрос, и мы ответим в течение 15 минут!",
        parse_mode='HTML'
    )

# Fallback обработчик для всех сообщений
@router.message()
async def handle_all_messages(message: Message):
    """Обработчик для всех остальных сообщений"""
    logger.info(f"📨 Получено сообщение от {message.from_user.id}: {message.text}")
    
    # Простой ответ на любое сообщение
    await message.answer("Привет! Используйте команду /start для начала работы.")
