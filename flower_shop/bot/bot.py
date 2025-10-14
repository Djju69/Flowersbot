"""
Telegram Bot для магазина цветов "Цветы Нячанг" - Гибридная архитектура
"""
import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

# Импортируем обработчики
from .handlers import start, orders, reminders, support, admin

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
WEBAPP_URL = os.getenv('WEBAPP_URL', 'https://flowersbot-production.up.railway.app/webapp')

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в переменных окружения")

async def main():
    """Основная функция запуска бота"""
    try:
        # Создаем бота и диспетчер
        bot = Bot(token=BOT_TOKEN)
        storage = MemoryStorage()
        dp = Dispatcher(storage=storage)
        
        # Регистрируем роутеры
        dp.include_router(start.router)
        dp.include_router(orders.router)
        dp.include_router(reminders.router)
        dp.include_router(support.router)
        dp.include_router(admin.router)
        
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
        try:
            webhook_info = await bot.get_webhook_info()
            logger.info(f"📊 Текущий webhook: {webhook_info.url}")
            
            if webhook_info.url != webhook_url:
                logger.info(f"🔄 Обновляем webhook с {webhook_info.url} на {webhook_url}")
                await bot.set_webhook(webhook_url)
                logger.info("✅ Webhook установлен успешно")
            else:
                logger.info("✅ Webhook уже установлен правильно")
        except Exception as e:
            logger.error(f"❌ Ошибка установки webhook: {e}")
            raise
        
        logger.info("🚀 Бот запущен успешно!")
        
        # Запускаем webhook сервер
        from aiohttp import web
        
        app = web.Application()
        
        # Добавляем health check endpoint для Railway
        async def health_check(request):
            return web.Response(text="OK", status=200)
        
        app.router.add_get("/health", health_check)
        
        # Добавляем тестовый endpoint для проверки webhook
        async def test_webhook(request):
            webhook_info = await bot.get_webhook_info()
            return web.Response(
                text=f"Webhook URL: {webhook_info.url}\nPending updates: {webhook_info.pending_update_count}",
                status=200
            )
        
        app.router.add_get("/test-webhook", test_webhook)
        
        # Webhook endpoint
        async def webhook_handler(request):
            try:
                data = await request.json()
                logger.info(f"📨 Получено обновление: {data.get('update_id', 'unknown')}")
                
                # Проверяем что это валидное обновление от Telegram
                if 'update_id' not in data:
                    logger.warning("⚠️ Невалидное обновление от Telegram")
                    return web.Response(text="INVALID", status=400)
                
                # Преобразуем dict в объект Update
                from aiogram.types import Update
                update = Update(**data)
                
                # Обрабатываем обновление
                await dp.feed_update(bot, update)
                logger.info("✅ Обновление обработано успешно")
                return web.Response(text="OK")
            except Exception as e:
                logger.error(f"❌ Ошибка в webhook handler: {e}")
                import traceback
                logger.error(f"❌ Traceback: {traceback.format_exc()}")
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
