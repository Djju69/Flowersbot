"""
Универсальный сервер для Bot + API
Объединяет Telegram Bot и FastAPI в одном процессе
"""
import asyncio
import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from aiohttp import web

# Загружаем переменные окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Получаем токен бота
BOT_TOKEN = os.getenv('BOT_TOKEN')
WEBAPP_URL = os.getenv('WEBAPP_URL', 'https://your-webapp-url.com')

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в переменных окружения")

# Создаем роутер для бота
bot_router = Router()

# Обработчики команд бота
@bot_router.message(CommandStart())
async def cmd_start(message: Message):
    """Приветствие и кнопка открытия Mini App"""
    
    # Inline кнопка с Mini App
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🛍 Открыть магазин",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )]
    ])
    
    text = """🌸 <b>Добро пожаловать в «Цветы Нячанг»!</b>

Свежие букеты с доставкой за 2-3 часа 🚚
📸 Фото перед отправкой
💳 Удобная оплата

Нажмите кнопку ниже чтобы открыть каталог:"""
    
    await message.answer(
        text,
        reply_markup=keyboard,
        parse_mode='HTML'
    )

# Глобальные переменные для бота
bot = None
dp = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление жизненным циклом приложения"""
    global bot, dp
    
    try:
        # Инициализируем бота
        bot = Bot(token=BOT_TOKEN)
        storage = MemoryStorage()
        dp = Dispatcher(storage=storage)
        dp.include_router(bot_router)
        
        # Настраиваем webhook
        webhook_path = "/webhook"
        port = int(os.getenv("PORT", 8000))
        
        railway_domain = os.getenv("RAILWAY_PUBLIC_DOMAIN")
        if railway_domain:
            webhook_url = f"https://{railway_domain}{webhook_path}"
        else:
            webhook_url = os.getenv("WEBHOOK_URL", f"https://your-domain.railway.app{webhook_path}")
        
        await bot.set_webhook(webhook_url)
        logger.info(f"🔗 Webhook установлен: {webhook_url}")
        
        yield
        
    finally:
        # Закрываем соединения
        if bot:
            await bot.session.close()

# Создаем FastAPI приложение
app = FastAPI(
    title="Flower Shop API + Bot",
    description="API для магазина цветов + Telegram Bot",
    version="1.0.0",
    lifespan=lifespan
)

# API Routes
@app.get("/")
async def root():
    return {"message": "Flower Shop API + Bot", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "OK", "bot": "active"}

@app.post("/webhook")
async def webhook_handler(request: web.Request):
    """Обработчик webhook от Telegram"""
    try:
        data = await request.json()
        await dp.feed_update(bot, data)
        return web.Response(text="OK")
    except Exception as e:
        logger.error(f"❌ Ошибка webhook: {e}")
        return web.Response(text="ERROR", status=500)

# API endpoints (здесь можно добавить FastAPI роуты)
@app.get("/api/products")
async def get_products():
    """Получить список товаров"""
    # Здесь будет логика получения товаров
    return {"products": []}

@app.post("/api/orders")
async def create_order():
    """Создать заказ"""
    # Здесь будет логика создания заказа
    return {"success": True, "order_id": 123}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
