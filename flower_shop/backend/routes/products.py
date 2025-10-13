"""
API роуты для товаров
"""
from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from models.database import Product, Base
from sqlalchemy import create_engine
import os

router = APIRouter()

# Подключение к БД
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/flowers')
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

@router.get("/products")
async def get_products(category: str = None, popular: bool = None):
    """Получить список товаров"""
    db = Session(engine)
    try:
        query = db.query(Product).filter(Product.is_available == True)
        
        if category:
            query = query.filter(Product.category == category)
        
        if popular is not None:
            query = query.filter(Product.is_popular == popular)
        
        products = query.all()
        return [
            {
                "id": p.id,
                "name": p.name,
                "category": p.category,
                "description": p.description,
                "price": p.price,
                "photo_url": p.photo_url,
                "is_popular": p.is_popular
            }
            for p in products
        ]
    finally:
        db.close()

@router.get("/products/{product_id}")
async def get_product(product_id: int):
    """Получить товар по ID"""
    db = Session(engine)
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return {
            "id": product.id,
            "name": product.name,
            "category": product.category,
            "description": product.description,
            "price": product.price,
            "photo_url": product.photo_url,
            "is_popular": product.is_popular
        }
    finally:
        db.close()

@router.post("/products")
async def create_product(product_data: dict):
    """Создать товар (для админа)"""
    db = Session(engine)
    try:
        product = Product(**product_data)
        db.add(product)
        db.commit()
        db.refresh(product)
        return {"id": product.id, "message": "Product created"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()

@router.patch("/products/{product_id}")
async def update_product(product_id: int, data: dict):
    """Обновить товар"""
    db = Session(engine)
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        for key, value in data.items():
            setattr(product, key, value)
        
        db.commit()
        return {"message": "Product updated"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()

@router.delete("/products/{product_id}")
async def delete_product(product_id: int):
    """Удалить товар"""
    db = Session(engine)
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        db.delete(product)
        db.commit()
        return {"message": "Product deleted"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()
