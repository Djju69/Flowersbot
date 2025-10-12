#!/usr/bin/env python3
"""
Простой запуск бота для совместимости с Railway
"""
import sys
import os

# Добавляем текущую директорию в путь
sys.path.insert(0, os.path.dirname(__file__))

# Импортируем и запускаем основной бот
from bot.bot import main
import asyncio

if __name__ == "__main__":
    asyncio.run(main())
