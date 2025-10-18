"""
FastAPI Backend для магазина цветов "Цветы Нячанг"
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import products, orders
from .models.database import create_tables
import asyncio
from starlette.middleware.sessions import SessionMiddleware
import os

app = FastAPI(title="Flowers Nha Trang API", version="1.0.0")

# CORS для Mini App
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Сессии для админ-панели
SESSION_SECRET = os.getenv("SESSION_SECRET", "change-me-please")
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET)

# Подключаем роуты
app.include_router(products.router, prefix="/api")
app.include_router(orders.router, prefix="/api")
try:
    from .admin.routes import router as admin_router
    app.include_router(admin_router)
except Exception:
    # Админ-панель не блокирует API при ошибках импорта
    pass

@app.on_event("startup")
async def startup_event():
    """Создаем таблицы при запуске (с защитой от временных сбоев БД)"""
    try:
        await create_tables()
    except Exception as e:
        # Не роняем приложение, чтобы health отвечал, а API мог подняться после восстановления БД
        import logging
        logging.getLogger(__name__).error(f"DB init error (startup skipped): {e}")

@app.get("/")
async def root():
    return {"message": "Flowers Nha Trang API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "OK"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
