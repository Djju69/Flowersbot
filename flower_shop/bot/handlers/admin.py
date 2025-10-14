"""
Обработчики для админ-панели
"""
import logging
import aiohttp
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import os

logger = logging.getLogger(__name__)
router = Router()

API_URL = os.getenv('API_URL', 'http://localhost:8000')
ADMIN_IDS = os.getenv('ADMIN_IDS', '').split(',')

class ProductStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_category = State()
    waiting_for_description = State()
    waiting_for_price = State()
    waiting_for_photo = State()

def is_admin(user_id: int) -> bool:
    """Проверить является ли пользователь админом"""
    return str(user_id) in ADMIN_IDS

async def get_products():
    """Получить список товаров из API"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_URL}/api/products") as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"Ошибка получения товаров: {response.status}")
                    return []
    except Exception as e:
        logger.error(f"Ошибка API запроса: {e}")
        return []

async def get_orders():
    """Получить список заказов из API"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_URL}/api/orders") as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"Ошибка получения заказов: {response.status}")
                    return []
    except Exception as e:
        logger.error(f"Ошибка API запроса: {e}")
        return []

@router.message(F.text == "/admin")
async def admin_menu(message: Message):
    """Админ-меню"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ У вас нет прав администратора.")
        return
    
    logger.info(f"🔧 Админ-меню от {message.from_user.id}")
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📦 Товары", callback_data="admin_products")],
        [InlineKeyboardButton(text="🛒 Заказы", callback_data="admin_orders")],
        [InlineKeyboardButton(text="➕ Добавить товар", callback_data="admin_add_product")],
        [InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats")]
    ])
    
    await message.answer(
        "🔧 <b>Админ-панель</b>\n\n"
        "Выберите действие:",
        reply_markup=keyboard,
        parse_mode='HTML'
    )

@router.callback_query(F.data == "admin_products")
async def admin_products_list(callback_query: CallbackQuery):
    """Список товаров для админа"""
    if not is_admin(callback_query.from_user.id):
        await callback_query.answer("❌ Нет прав администратора")
        return
    
    products = await get_products()
    
    if not products:
        await callback_query.message.edit_text(
            "📦 <b>Товары</b>\n\n"
            "Товары не найдены.",
            parse_mode='HTML'
        )
        await callback_query.answer()
        return
    
    text = "📦 <b>Список товаров:</b>\n\n"
    
    for product in products[:10]:  # Показываем первые 10
        text += f"🆔 {product['id']} - {product['name']}\n"
        text += f"💰 {product['price']:,} VND\n"
        text += f"📂 {product['category']}\n\n"
    
    if len(products) > 10:
        text += f"... и еще {len(products) - 10} товаров"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Добавить товар", callback_data="admin_add_product")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="admin_back")]
    ])
    
    await callback_query.message.edit_text(
        text,
        reply_markup=keyboard,
        parse_mode='HTML'
    )
    
    await callback_query.answer()

@router.callback_query(F.data == "admin_orders")
async def admin_orders_list(callback_query: CallbackQuery):
    """Список заказов для админа"""
    if not is_admin(callback_query.from_user.id):
        await callback_query.answer("❌ Нет прав администратора")
        return
    
    orders = await get_orders()
    
    if not orders:
        await callback_query.message.edit_text(
            "🛒 <b>Заказы</b>\n\n"
            "Заказы не найдены.",
            parse_mode='HTML'
        )
        await callback_query.answer()
        return
    
    text = "🛒 <b>Последние заказы:</b>\n\n"
    
    for order in orders[:5]:  # Показываем последние 5
        status_emoji = {
            'pending': '⏳',
            'confirmed': '✅',
            'making': '🌸',
            'delivering': '🚚',
            'delivered': '🎉',
            'cancelled': '❌'
        }.get(order['status'], '❓')
        
        text += f"{status_emoji} <b>Заказ #{order['id']}</b>\n"
        text += f"👤 {order['name']} - {order['phone']}\n"
        text += f"💰 {order['total']:,} VND\n"
        text += f"📅 {order['delivery_date']} в {order['delivery_time']}\n\n"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="admin_back")]
    ])
    
    await callback_query.message.edit_text(
        text,
        reply_markup=keyboard,
        parse_mode='HTML'
    )
    
    await callback_query.answer()

@router.callback_query(F.data == "admin_add_product")
async def admin_add_product_start(callback_query: CallbackQuery, state: FSMContext):
    """Начать добавление товара"""
    if not is_admin(callback_query.from_user.id):
        await callback_query.answer("❌ Нет прав администратора")
        return
    
    await state.set_state(ProductStates.waiting_for_name)
    
    await callback_query.message.edit_text(
        "➕ <b>Добавить товар</b>\n\n"
        "📝 Введите название товара:",
        parse_mode='HTML'
    )
    
    await callback_query.answer()

@router.message(ProductStates.waiting_for_name)
async def process_product_name(message: Message, state: FSMContext):
    """Обработать название товара"""
    await state.update_data(name=message.text.strip())
    await state.set_state(ProductStates.waiting_for_category)
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌹 Розы", callback_data="cat_roses")],
        [InlineKeyboardButton(text="🌺 Экзотика", callback_data="cat_exotic")],
        [InlineKeyboardButton(text="💐 Микс", callback_data="cat_mix")],
        [InlineKeyboardButton(text="🤍 Моно", callback_data="cat_mono")]
    ])
    
    await message.answer(
        f"📂 <b>Выберите категорию:</b>\n\n"
        f"Товар: {message.text.strip()}",
        reply_markup=keyboard,
        parse_mode='HTML'
    )

@router.callback_query(F.data.startswith("cat_"))
async def process_product_category(callback_query: CallbackQuery, state: FSMContext):
    """Обработать категорию товара"""
    category = callback_query.data.replace("cat_", "")
    
    category_names = {
        'roses': '🌹 Розы',
        'exotic': '🌺 Экзотика',
        'mix': '💐 Микс',
        'mono': '🤍 Моно'
    }
    
    await state.update_data(category=category)
    await state.set_state(ProductStates.waiting_for_description)
    
    await callback_query.message.edit_text(
        f"📝 <b>Введите описание товара:</b>\n\n"
        f"Категория: {category_names[category]}",
        parse_mode='HTML'
    )
    
    await callback_query.answer()

@router.message(ProductStates.waiting_for_description)
async def process_product_description(message: Message, state: FSMContext):
    """Обработать описание товара"""
    await state.update_data(description=message.text.strip())
    await state.set_state(ProductStates.waiting_for_price)
    
    await message.answer(
        f"💰 <b>Введите цену в VND:</b>\n\n"
        f"Например: 800000",
        parse_mode='HTML'
    )

@router.message(ProductStates.waiting_for_price)
async def process_product_price(message: Message, state: FSMContext):
    """Обработать цену товара"""
    try:
        price = int(message.text.strip())
        if price <= 0:
            await message.answer("❌ Цена должна быть больше 0. Попробуйте еще раз:")
            return
    except ValueError:
        await message.answer("❌ Неверный формат цены. Введите число:")
        return
    
    await state.update_data(price=price)
    await state.set_state(ProductStates.waiting_for_photo)
    
    await message.answer(
        f"📸 <b>Введите URL фото товара:</b>\n\n"
        f"Или отправьте 'skip' чтобы пропустить",
        parse_mode='HTML'
    )

@router.message(ProductStates.waiting_for_photo)
async def process_product_photo(message: Message, state: FSMContext):
    """Обработать фото товара"""
    photo_url = message.text.strip()
    
    if photo_url.lower() == 'skip':
        photo_url = "https://images.unsplash.com/photo-1518895949257-7621c3c786d7?w=400"
    
    await state.update_data(photo_url=photo_url)
    
    # Создаем товар
    data = await state.get_data()
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{API_URL}/api/products", json={
                "name": data['name'],
                "category": data['category'],
                "description": data['description'],
                "price": data['price'],
                "photo_url": photo_url,
                "is_available": True,
                "is_popular": False
            }) as response:
                if response.status == 200:
                    result = await response.json()
                    await message.answer(
                        f"✅ <b>Товар добавлен!</b>\n\n"
                        f"🆔 ID: {result['id']}\n"
                        f"📝 Название: {data['name']}\n"
                        f"💰 Цена: {data['price']:,} VND",
                        parse_mode='HTML'
                    )
                else:
                    await message.answer(
                        "❌ <b>Ошибка</b>\n\n"
                        "Не удалось добавить товар. Попробуйте позже.",
                        parse_mode='HTML'
                    )
    except Exception as e:
        logger.error(f"Ошибка создания товара: {e}")
        await message.answer(
            "❌ <b>Ошибка</b>\n\n"
            "Не удалось добавить товар. Попробуйте позже.",
            parse_mode='HTML'
        )
    
    await state.clear()

@router.callback_query(F.data == "admin_back")
async def admin_back(callback_query: CallbackQuery):
    """Вернуться в админ-меню"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📦 Товары", callback_data="admin_products")],
        [InlineKeyboardButton(text="🛒 Заказы", callback_data="admin_orders")],
        [InlineKeyboardButton(text="➕ Добавить товар", callback_data="admin_add_product")],
        [InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats")]
    ])
    
    await callback_query.message.edit_text(
        "🔧 <b>Админ-панель</b>\n\n"
        "Выберите действие:",
        reply_markup=keyboard,
        parse_mode='HTML'
    )
    
    await callback_query.answer()
