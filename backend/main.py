"""
FastAPI Backend для Telegram Mini App "Цветы Нячанг"
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Создаем FastAPI приложение
app = FastAPI(
    title="Flower Shop API",
    description="API для магазина цветов в Нячанге",
    version="1.0.0"
)

# Настройка CORS для webapp
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Настройка базы данных
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL or "sqlite:///./flowers.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Модели базы данных
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
    is_express = Column(Boolean, default=False)

class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    
    # Контакты
    telegram_id = Column(Integer, nullable=False, index=True)
    telegram_username = Column(String(100))
    name = Column(String(200))  # Имя заказчика из Telegram
    
    # Получатель (ОБЯЗАТЕЛЬНО)
    recipient_name = Column(String(200), nullable=False)  # Имя получателя цветов
    
    # Контакт для связи (ОБЯЗАТЕЛЬНО)
    contact_type = Column(String(20), nullable=False)  # telegram, whatsapp, zalo
    contact_value = Column(String(100), nullable=False)  # username или номер
    
    # Доставка
    latitude = Column(String(50), nullable=False)  # ОБЯЗАТЕЛЬНО - геолокация Google
    longitude = Column(String(50), nullable=False)  # ОБЯЗАТЕЛЬНО
    address_text = Column(Text)  # Опционально - текстовое описание адреса
    
    # Дата и время (ОБЯЗАТЕЛЬНО)
    delivery_date = Column(String(50), nullable=False)
    delivery_time = Column(String(50), nullable=False)
    
    # Дополнительно
    card_text = Column(Text)
    is_anonymous = Column(Boolean, default=False)
    
    # Финансы
    items_total = Column(Integer)  # В VND
    delivery_cost = Column(Integer)  # В VND
    total = Column(Integer)  # В VND
    
    # Статус
    status = Column(String(50), default='pending')
    # pending, confirmed, making, delivering, delivered, cancelled
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    items = relationship('OrderItem', back_populates='order')

class OrderItem(Base):
    __tablename__ = 'order_items'
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_name = Column(String(200))
    product_photo = Column(String(500))
    size = Column(String(20))  # standard, large, xl
    price = Column(Integer)  # В VND
    quantity = Column(Integer, default=1)
    
    order = relationship('Order', back_populates='items')

# Pydantic модели для API
class ProductResponse(BaseModel):
    id: int
    name: str
    category: Optional[str]
    description: Optional[str]
    price: int  # В VND
    photo_url: Optional[str]
    is_available: bool
    is_popular: bool
    is_express: bool
    
    class Config:
        from_attributes = True

class OrderItemCreate(BaseModel):
    product_id: int
    product_name: str
    product_photo: str
    size: str
    price: int  # В VND
    quantity: int = 1

class OrderCreate(BaseModel):
    # Контакты
    telegram_id: int
    telegram_username: Optional[str]
    name: str  # Имя заказчика из Telegram
    
    # Получатель (ОБЯЗАТЕЛЬНО)
    recipient_name: str  # Имя получателя цветов
    
    # Контакт для связи (ОБЯЗАТЕЛЬНО)
    contact_type: str  # telegram, whatsapp, zalo
    contact_value: str  # username или номер
    
    # Доставка
    latitude: str  # ОБЯЗАТЕЛЬНО - геолокация Google
    longitude: str  # ОБЯЗАТЕЛЬНО
    address_text: Optional[str] = None  # Опционально - текстовое описание
    
    # Дата и время (ОБЯЗАТЕЛЬНО)
    delivery_date: str
    delivery_time: str
    
    # Дополнительно
    card_text: Optional[str] = None
    is_anonymous: bool = False
    
    # Товары
    items: List[OrderItemCreate]
    
    # Финансы (рассчитываются на фронте)
    items_total: int  # В VND
    delivery_cost: int  # В VND
    total: int  # В VND
    
    @validator('contact_type')
    def validate_contact_type(cls, v):
        if v not in ['telegram', 'whatsapp', 'zalo']:
            raise ValueError('Тип контакта должен быть: telegram, whatsapp или zalo')
        return v
    
    @validator('contact_value')
    def validate_contact_value(cls, v):
        if len(v.strip()) < 3:
            raise ValueError('Контакт должен содержать минимум 3 символа')
        return v.strip()
    
    @validator('recipient_name')
    def validate_recipient_name(cls, v):
        if len(v.strip()) < 2:
            raise ValueError('Имя получателя должно содержать минимум 2 символа')
        return v.strip()

class OrderResponse(BaseModel):
    success: bool
    order_id: int
    message: str

# Создаем таблицы
Base.metadata.create_all(bind=engine)

# Dependency для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API Routes
@app.get("/")
async def root():
    return {"message": "Flower Shop API", "version": "1.0.0"}

@app.get("/api/products", response_model=List[ProductResponse])
async def get_products(
    category: Optional[str] = None,
    popular: Optional[bool] = None,
    db: SessionLocal = None
):
    """Получить список товаров"""
    if db is None:
        db = SessionLocal()
    
    try:
        query = db.query(Product).filter(Product.is_available == True)
        
        if category:
            query = query.filter(Product.category == category)
        
        if popular is not None:
            query = query.filter(Product.is_popular == popular)
        
        products = query.all()
        return products
    finally:
        db.close()

@app.get("/api/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int):
    """Получить один товар"""
    db = SessionLocal()
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Товар не найден")
        return product
    finally:
        db.close()

@app.post("/api/orders", response_model=OrderResponse)
async def create_order(order: OrderCreate):
    """Создать заказ"""
    db = SessionLocal()
    try:
        # Создаем заказ
        db_order = Order(
            telegram_id=order.telegram_id,
            telegram_username=order.telegram_username,
            name=order.name,
            recipient_name=order.recipient_name,
            contact_type=order.contact_type,
            contact_value=order.contact_value,
            latitude=order.latitude,
            longitude=order.longitude,
            address_text=order.address_text,
            delivery_date=order.delivery_date,
            delivery_time=order.delivery_time,
            card_text=order.card_text,
            is_anonymous=order.is_anonymous,
            items_total=order.items_total,
            delivery_cost=order.delivery_cost,
            total=order.total
        )
        
        db.add(db_order)
        db.flush()  # Получаем ID заказа
        
        # Добавляем товары
        for item in order.items:
            db_item = OrderItem(
                order_id=db_order.id,
                product_name=item.product_name,
                product_photo=item.product_photo,
                size=item.size,
                price=item.price,
                quantity=item.quantity
            )
            db.add(db_item)
        
        db.commit()
        
        # Отправляем уведомление в Telegram Bot
        from utils.telegram_notify import send_order_notification
        await send_order_notification(db_order.id, order.dict())
        
        return OrderResponse(
            success=True,
            order_id=db_order.id,
            message="Заказ принят! Ожидайте подтверждения."
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.get("/api/orders/{telegram_id}")
async def get_user_orders(telegram_id: int):
    """Получить заказы пользователя"""
    db = SessionLocal()
    try:
        orders = db.query(Order).filter(Order.telegram_id == telegram_id).order_by(Order.created_at.desc()).all()
        return orders
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
