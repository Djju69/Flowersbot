"""
API роуты для заказов
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models.database import Order, OrderItem, Product, Base, get_db
from ..utils.telegram_notify import send_order_notification
import os

router = APIRouter()

@router.post("/orders")
async def create_order(order_data: dict, db: AsyncSession = Depends(get_db)):
    """Создать заказ"""
    try:
        # Создаем заказ
        order = Order(
            telegram_id=order_data['telegram_id'],
            telegram_username=order_data.get('telegram_username'),
            name=order_data['name'],
            phone=order_data['phone'],
            address=order_data['address'],
            latitude=order_data.get('latitude'),
            longitude=order_data.get('longitude'),
            delivery_date=order_data['delivery_date'],
            delivery_time=order_data['delivery_time'],
            card_text=order_data.get('card_text'),
            is_anonymous=order_data.get('is_anonymous', False),
            items_total=order_data['items_total'],
            delivery_cost=order_data['delivery_cost'],
            total=order_data['total']
        )
        
        db.add(order)
        await db.flush()  # Получаем ID заказа
        
        # Добавляем товары
        for item in order_data['items']:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item['product_id'],
                product_name=item['product_name'],
                size=item.get('size', 'standard'),
                price=item['price'],
                quantity=item['quantity']
            )
            db.add(order_item)
        
        await db.commit()
        
        # Отправляем уведомления
        await send_order_notification(order.id, order_data)
        
        return {"order_id": order.id, "message": "Order created successfully"}
        
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/orders/{telegram_id}")
async def get_user_orders(telegram_id: int, db: AsyncSession = Depends(get_db)):
    """Получить заказы пользователя"""
    try:
        result = await db.execute(
            select(Order)
            .where(Order.telegram_id == telegram_id)
            .order_by(Order.created_at.desc())
        )
        orders = result.scalars().all()
        
        return [
            {
                "id": order.id,
                "status": order.status,
                "total": order.total,
                "delivery_date": order.delivery_date,
                "delivery_time": order.delivery_time,
                "created_at": order.created_at.isoformat(),
                "items": [
                    {
                        "product_name": item.product_name,
                        "size": item.size,
                        "price": item.price,
                        "quantity": item.quantity
                    }
                    for item in order.items
                ]
            }
            for order in orders
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/orders/{order_id}/status")
async def update_order_status(order_id: int, status: str, db: AsyncSession = Depends(get_db)):
    """Обновить статус заказа (для админа)"""
    try:
        result = await db.execute(select(Order).where(Order.id == order_id))
        order = result.scalar_one_or_none()
        
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        order.status = status
        await db.commit()
        
        return {"message": "Order status updated"}
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
