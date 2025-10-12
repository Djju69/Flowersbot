"""
Telegram Bot для магазина цветов "Цветы Нячанг"
"""
import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

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

# Создаем роутер
router = Router()

# Обработчики команд
@router.message(CommandStart())
async def cmd_start(message: Message):
    """Приветствие и кнопка открытия Mini App"""
    
    logger.info(f"🎯 Получена команда /start от пользователя {message.from_user.id}")
    
    webapp_url = os.getenv('WEBAPP_URL', 'https://your-webapp-url.com')
    
    # Inline кнопка с Mini App
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🛍 Открыть магазин",
            web_app=WebAppInfo(url=webapp_url)
        )]
    ])
    
    text = """🌸 <b>Добро пожаловать в «Цветы Нячанг»!</b>

Свежие букеты с доставкой за 2-3 часа 🚚
📸 Фото перед отправкой
💳 Удобная оплата

Нажмите кнопку ниже чтобы открыть каталог:"""
    
    try:
        await message.answer(
            text,
            reply_markup=keyboard,
            parse_mode='HTML'
        )
        logger.info(f"✅ Ответ отправлен пользователю {message.from_user.id}")
    except Exception as e:
        logger.error(f"❌ Ошибка отправки ответа: {e}")

# Fallback обработчик для всех сообщений
@router.message()
async def handle_all_messages(message: Message):
    """Обработчик для всех остальных сообщений"""
    logger.info(f"📨 Получено сообщение от {message.from_user.id}: {message.text}")
    
    # Простой ответ на любое сообщение
    await message.answer("Привет! Используйте команду /start для начала работы.")

async def main():
    """Основная функция запуска бота"""
    try:
        # Создаем бота и диспетчер
        bot = Bot(token=BOT_TOKEN)
        storage = MemoryStorage()
        dp = Dispatcher(storage=storage)
        
        # Регистрируем роутер
        dp.include_router(router)
        
        # Настраиваем webhook для Railway
        webhook_path = "/webhook"
        port = int(os.getenv("PORT", 8000))
        
        # Получаем домен Railway из переменных окружения
        railway_domain = os.getenv("RAILWAY_PUBLIC_DOMAIN")
        if railway_domain:
            webhook_url = f"https://{railway_domain}{webhook_path}"
        else:
            webhook_url = os.getenv("WEBHOOK_URL", f"https://your-domain.railway.app{webhook_path}")
        
        # Устанавливаем webhook
        logger.info(f"🔗 Устанавливаем webhook: {webhook_url}")
        await bot.set_webhook(webhook_url)
        
        logger.info("🚀 Бот запущен успешно!")
        
        # Запускаем webhook сервер
        from aiohttp import web
        
        app = web.Application()
        
        # Добавляем health check endpoint для Railway
        async def health_check(request):
            return web.Response(text="OK", status=200)
        
        app.router.add_get("/health", health_check)
        
        # Webhook endpoint
        async def webhook_handler(request):
            try:
                data = await request.json()
                logger.info(f"📨 Получено обновление: {data.get('update_id', 'unknown')}")
                await dp.feed_update(bot, data)
                logger.info("✅ Обновление обработано успешно")
                return web.Response(text="OK")
            except Exception as e:
                logger.error(f"❌ Ошибка в webhook handler: {e}")
                return web.Response(text="ERROR", status=500)
        
        app.router.add_post(webhook_path, webhook_handler)
        
        # Запускаем сервер
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, '0.0.0.0', port)
        await site.start()
        
        logger.info(f"🌐 Webhook сервер запущен на порту {port}")
        
        # Держим сервер запущенным
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("🛑 Получен сигнал остановки")
        
    except Exception as e:
        logger.error(f"❌ Ошибка запуска бота: {e}")
        raise
    finally:
        # Закрываем соединения
        if 'bot' in locals():
            await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
