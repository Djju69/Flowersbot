#!/usr/bin/env python3
"""
Скрипт для запуска Backend API и Bot одновременно
"""
import asyncio
import subprocess
import os
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start_backend():
    """Запуск Backend API"""
    logger.info("🚀 Запуск Backend API...")
    process = subprocess.Popen([
        sys.executable, "-m", "uvicorn", 
        "backend.main:app", 
        "--host", "0.0.0.0", 
        "--port", os.getenv("PORT", "8000")
    ], cwd="flower_shop")
    return process

async def start_bot():
    """Запуск Bot"""
    logger.info("🤖 Запуск Bot...")
    process = subprocess.Popen([
        sys.executable, "bot/bot.py"
    ], cwd="flower_shop")
    return process

async def main():
    """Запуск всех сервисов"""
    try:
        logger.info("🌸 Запуск Цветы Нячанг...")
        
        # Запускаем Backend
        backend_process = await start_backend()
        
        # Ждем немного чтобы Backend запустился
        await asyncio.sleep(3)
        
        # Запускаем Bot
        bot_process = await start_bot()
        
        logger.info("✅ Все сервисы запущены!")
        
        # Ждем завершения
        await asyncio.gather(
            asyncio.create_task(asyncio.to_thread(backend_process.wait)),
            asyncio.create_task(asyncio.to_thread(bot_process.wait))
        )
        
    except KeyboardInterrupt:
        logger.info("🛑 Остановка сервисов...")
        backend_process.terminate()
        bot_process.terminate()
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
