"""
Telegram Bot для заказа цветов в Нячанге
Создан по ТЗ - точно как указано в требованиях
"""
import os
import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
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
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в переменных окружения")

async def main():
    """Основная функция запуска бота"""
    try:
        # Создаем бота и диспетчер
        bot = Bot(token=BOT_TOKEN)
        storage = MemoryStorage()
        dp = Dispatcher(storage=storage)
        
        # Импортируем и регистрируем обработчики
        from handlers import start_handler
        
        # Регистрируем обработчики
        dp.message.register(start_handler.cmd_start, lambda message: message.text == "/start")
        dp.message.register(start_handler.shop_button, lambda message: message.text == "🛍 Магазин")
        dp.message.register(start_handler.repeat_button, lambda message: message.text == "🔁 Повторить")
        dp.message.register(start_handler.orders_button, lambda message: message.text == "📦 Мои заказы")
        dp.message.register(start_handler.support_button, lambda message: message.text == "💬 Поддержка")
        
        # Настраиваем webhook для Railway
        webhook_path = "/webhook"
        port = int(os.getenv("PORT", 8000))
        
        # Получаем домен Railway из переменных окружения
        railway_domain = os.getenv("RAILWAY_PUBLIC_DOMAIN")
        if railway_domain:
            webhook_url = f"https://{railway_domain}{webhook_path}"
        else:
            webhook_url = os.getenv("WEBHOOK_URL", f"https://flowersbot-production.up.railway.app{webhook_path}")
        
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
        app = web.Application()
        
        # Настраиваем webhook handler
        webhook_requests_handler = SimpleRequestHandler(
            dispatcher=dp,
            bot=bot,
        )
        webhook_requests_handler.register(app, path=webhook_path)
        
        # Настраиваем приложение
        setup_application(app, dp, bot=bot)
        
        # Запускаем сервер
        logger.info(f"🌐 Webhook сервер запущен на порту {port}")
        await web._run_app(app, host="0.0.0.0", port=port)
        
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")
        raise
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"❌ Фатальная ошибка: {e}")
        raise
