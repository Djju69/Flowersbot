"""
API роуты для товаров
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models.database import Product, Base, get_db
import os

router = APIRouter()

# Создаем таблицы при запуске
async def create_tables():
    from models.database import engine, Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@router.get("/products")
async def get_products(category: str = None, popular: bool = None, db: AsyncSession = Depends(get_db)):
    """Получить список товаров"""
    try:
        query = select(Product).where(Product.is_available == True)
        
        if category:
            query = query.where(Product.category == category)
        
        if popular is not None:
            query = query.where(Product.is_popular == popular)
        
        result = await db.execute(query)
        products = result.scalars().all()
        
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/products/{product_id}")
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    """Получить товар по ID"""
    try:
        result = await db.execute(select(Product).where(Product.id == product_id))
        product = result.scalar_one_or_none()
        
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
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/products")
async def create_product(product_data: dict, db: AsyncSession = Depends(get_db)):
    """Создать товар (для админа)"""
    try:
        product = Product(**product_data)
        db.add(product)
        await db.commit()
        await db.refresh(product)
        return {"id": product.id, "message": "Product created"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/products/{product_id}")
async def update_product(product_id: int, data: dict, db: AsyncSession = Depends(get_db)):
    """Обновить товар"""
    try:
        result = await db.execute(select(Product).where(Product.id == product_id))
        product = result.scalar_one_or_none()
        
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        for key, value in data.items():
            setattr(product, key, value)
        
        await db.commit()
        return {"message": "Product updated"}
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/products/{product_id}")
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    """Удалить товар"""
    try:
        result = await db.execute(select(Product).where(Product.id == product_id))
        product = result.scalar_one_or_none()
        
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        await db.delete(product)
        await db.commit()
        return {"message": "Product deleted"}
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
