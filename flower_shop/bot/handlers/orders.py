"""
Обработчики для работы с заказами
"""
import logging
import aiohttp
from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import os

logger = logging.getLogger(__name__)
router = Router()

API_URL = os.getenv('API_URL', 'http://localhost:8000')
WEBAPP_URL = os.getenv('WEBAPP_URL', 'https://flowersbot-production.up.railway.app/webapp')

async def get_user_orders(telegram_id: int):
    """Получить заказы пользователя из API"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_URL}/api/orders/{telegram_id}") as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"Ошибка получения заказов: {response.status}")
                    return []
    except Exception as e:
        logger.error(f"Ошибка API запроса: {e}")
        return []

@router.message(F.text == "📦 Мои заказы")
async def my_orders(message: Message):
    """История заказов пользователя"""
    logger.info(f"📦 Запрос истории заказов от {message.from_user.id}")
    
    orders = await get_user_orders(message.from_user.id)
    
    if not orders:
        await message.answer(
            "📦 <b>Ваши заказы</b>\n\n"
            "У вас пока нет заказов.\n"
            "Нажмите /start чтобы сделать первый заказ!",
            parse_mode='HTML'
        )
        return
    
    text = "📦 <b>Ваши заказы:</b>\n\n"
    
    for order in orders[:5]:  # Показываем последние 5 заказов
        status_emoji = {
            'pending': '⏳',
            'confirmed': '✅',
            'making': '🌸',
            'delivering': '🚚',
            'delivered': '🎉',
            'cancelled': '❌'
        }.get(order['status'], '❓')
        
        text += f"{status_emoji} <b>Заказ #{order['id']}</b>\n"
        text += f"💰 {order['total']:,} VND\n"
        text += f"📅 {order['delivery_date']} в {order['delivery_time']}\n"
        text += f"Статус: {order['status']}\n\n"
    
    if len(orders) > 5:
        text += f"... и еще {len(orders) - 5} заказов"
    
    await message.answer(text, parse_mode='HTML')

@router.message(F.text == "🔁 Повторить")
async def repeat_last_order(message: Message):
    """Повторить последний заказ"""
    logger.info(f"🔁 Запрос повтора заказа от {message.from_user.id}")
    
    orders = await get_user_orders(message.from_user.id)
    
    if not orders:
        await message.answer(
            "🔁 <b>Повторить заказ</b>\n\n"
            "У вас пока нет заказов для повтора.\n"
            "Нажмите /start чтобы сделать первый заказ!",
            parse_mode='HTML'
        )
        return
    
    last_order = orders[0]  # Самый последний заказ
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=f"🛍 Повторить заказ #{last_order['id']}",
            web_app=WebAppInfo(url=f"{WEBAPP_URL}?repeat={last_order['id']}")
        )]
    ])
    
    # Формируем описание товаров
    items_text = ""
    for item in last_order['items']:
        items_text += f"• {item['product_name']} ({item['size']}) x{item['quantity']}\n"
    
    await message.answer(
        f"🔁 <b>Повторить последний заказ</b>\n\n"
        f"📦 Заказ #{last_order['id']}\n"
        f"💰 {last_order['total']:,} VND\n\n"
        f"<b>Товары:</b>\n{items_text}\n"
        f"Нажмите кнопку чтобы повторить:",
        reply_markup=keyboard,
        parse_mode='HTML'
    )

@router.callback_query(F.data.startswith("repeat_order_"))
async def repeat_specific_order(callback_query):
    """Повторить конкретный заказ"""
    order_id = callback_query.data.replace("repeat_order_", "")
    logger.info(f"🔄 Повтор заказа #{order_id} от {callback_query.from_user.id}")
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=f"🛍 Повторить заказ #{order_id}",
            web_app=WebAppInfo(url=f"{WEBAPP_URL}?repeat={order_id}")
        )]
    ])
    
    await callback_query.message.edit_text(
        f"🔄 <b>Повторить заказ #{order_id}</b>\n\n"
        f"Нажмите кнопку чтобы повторить этот заказ:",
        reply_markup=keyboard,
        parse_mode='HTML'
    )
    
    await callback_query.answer()

