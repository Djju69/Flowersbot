"""
Модели базы данных для магазина цветов
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

Base = declarative_base()

# Подключение к БД
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/flowers')
"""Нормализуем URL для asyncpg: поддерживаем оба префикса postgres:// и postgresql://"""
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql+asyncpg://', 1)
elif DATABASE_URL.startswith('postgresql://'):
    DATABASE_URL = DATABASE_URL.replace('postgresql://', 'postgresql+asyncpg://', 1)

engine = create_async_engine(DATABASE_URL)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with async_session() as session:
        yield session

async def create_tables():
    """Создание таблиц в базе данных"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    category = Column(String(50))  # roses, exotic, mix, mono
    description = Column(Text)
    price = Column(Integer, nullable=False)  # В VND
    photo_url = Column(String(500))
    is_available = Column(Boolean, default=True)
    is_popular = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, nullable=False)
    telegram_username = Column(String(100))
    name = Column(String(200))
    phone = Column(String(20), nullable=False)  # ОБЯЗАТЕЛЬНО
    address = Column(Text, nullable=False)
    latitude = Column(String(50))  # Геолокация
    longitude = Column(String(50))
    delivery_date = Column(String(50))
    delivery_time = Column(String(50))
    card_text = Column(Text)
    is_anonymous = Column(Boolean, default=False)
    items_total = Column(Integer)  # В VND
    delivery_cost = Column(Integer)
    total = Column(Integer)
    status = Column(String(50), default='pending')  # pending, confirmed, making, delivering, delivered, cancelled
    created_at = Column(DateTime, default=datetime.utcnow)
    
    items = relationship('OrderItem', back_populates='order')

class OrderItem(Base):
    __tablename__ = 'order_items'
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    product_name = Column(String(200))
    size = Column(String(20), default='standard')  # standard, large, xl
    price = Column(Integer)  # Цена за единицу в VND
    quantity = Column(Integer, default=1)
    
    order = relationship('Order', back_populates='items')
    product = relationship('Product')

class Reminder(Base):
    __tablename__ = 'reminders'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, nullable=False)
    event_name = Column(String(200), nullable=False)
    event_date = Column(String(50), nullable=False)  # DD.MM.YYYY
    remind_days_before = Column(Integer, default=3)  # За сколько дней напомнить
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
