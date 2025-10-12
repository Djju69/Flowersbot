#!/usr/bin/env python3
"""
Простой запуск бота для совместимости с Railway
"""
import sys
import os

# Добавляем путь к папке bot
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'bot'))

# Импортируем и запускаем основной бот
from bot import main
import asyncio

if __name__ == "__main__":
    asyncio.run(main())
