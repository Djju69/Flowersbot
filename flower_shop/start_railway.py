#!/usr/bin/env python3
"""
Скрипт для запуска Backend API и Bot одновременно на Railway
"""
import asyncio
import subprocess
import os
import sys
import logging
import signal
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def signal_handler(signum, frame):
    logger.info("🛑 Получен сигнал остановки")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

async def start_backend():
    """Запуск Backend API"""
    logger.info("🚀 Запуск Backend API...")
    process = subprocess.Popen([
        sys.executable, "-m", "uvicorn", 
        "main:app", 
        "--host", "0.0.0.0", 
        "--port", os.getenv("PORT", "8000")
    ], cwd="flower_shop/backend")
    return process

async def start_bot():
    """Запуск Bot"""
    logger.info("🤖 Запуск Bot...")
    process = subprocess.Popen([
        sys.executable, "bot.py"
    ], cwd="flower_shop/bot")
    return process

async def main():
    """Запуск всех сервисов"""
    try:
        logger.info("🌸 Запуск Цветы Нячанг на Railway...")
        
        # Запускаем Backend
        backend_process = await start_backend()
        
        # Ждем немного чтобы Backend запустился
        await asyncio.sleep(5)
        
        # Запускаем Bot
        bot_process = await start_bot()
        
        logger.info("✅ Все сервисы запущены!")
        logger.info(f"🌐 Backend API: http://0.0.0.0:{os.getenv('PORT', '8000')}")
        logger.info("🤖 Bot: webhook активен")
        
        # Ждем завершения
        while True:
            if backend_process.poll() is not None:
                logger.error("❌ Backend процесс завершился!")
                break
            if bot_process.poll() is not None:
                logger.error("❌ Bot процесс завершился!")
                break
            await asyncio.sleep(1)
        
    except KeyboardInterrupt:
        logger.info("🛑 Остановка сервисов...")
        backend_process.terminate()
        bot_process.terminate()
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")
        raise
    finally:
        # Закрываем процессы
        if 'backend_process' in locals():
            backend_process.terminate()
        if 'bot_process' in locals():
            bot_process.terminate()

if __name__ == "__main__":
    asyncio.run(main())
