#!/usr/bin/env python3
"""
Простой запуск backend для совместимости с Railway
"""
import sys
import os

# Добавляем путь к папке backend
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Импортируем и запускаем FastAPI
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
