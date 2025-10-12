"""
Telegram Bot для магазина цветов "Цветы Нячанг"
"""
import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import WebAppInfo
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

async def main():
    """Основная функция запуска бота"""
    try:
        # Создаем бота и диспетчер
        bot = Bot(token=BOT_TOKEN)
        storage = MemoryStorage()
        dp = Dispatcher(storage=storage)
        
        logger.info("🚀 Бот запущен успешно!")
        
        # Запускаем бота
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f"❌ Ошибка запуска бота: {e}")
        raise
    finally:
        # Закрываем соединения
        if 'bot' in locals():
            await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
