"""
Скрипт для добавления тестовых товаров в базу данных
"""
import asyncio
import sys
import os

# Добавляем путь к backend
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.main import engine, Product, Base
from sqlalchemy.orm import sessionmaker

# Создаем сессию
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def add_test_products():
    """Добавляем тестовые товары"""
    
    # Создаем таблицы
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Проверяем, есть ли уже товары
        existing_count = db.query(Product).count()
        if existing_count > 0:
            print(f"В базе уже есть {existing_count} товаров")
            return
        
        # Тестовые товары (цены в VND)
        products = [
            {
                "name": "🌹 Розы классические",
                "category": "roses",
                "description": "Красные розы в красивой упаковке. Идеально для романтических моментов.",
                "price": 800000,  # 800,000 VND
                "photo_url": "https://images.unsplash.com/photo-1518895949257-7621c3c786d7?w=400",
                "is_popular": True,
                "is_express": True
            },
            {
                "name": "🌺 Тропический рай",
                "category": "exotic",
                "description": "Экзотические цветы из тропиков. Яркие и необычные.",
                "price": 1200000,  # 1,200,000 VND
                "photo_url": "https://images.unsplash.com/photo-1563241527-3004b7be0ffd?w=400",
                "is_popular": True,
                "is_express": False
            },
            {
                "name": "💐 Весенний микс",
                "category": "mix",
                "description": "Смесь весенних цветов разных оттенков. Свежесть и красота.",
                "price": 900000,  # 900,000 VND
                "photo_url": "https://images.unsplash.com/photo-1490750967868-88aa4486c946?w=400",
                "is_popular": False,
                "is_express": True
            },
            {
                "name": "🤍 Белые лилии",
                "category": "mono",
                "description": "Элегантные белые лилии. Чистота и нежность.",
                "price": 700000,  # 700,000 VND
                "photo_url": "https://images.unsplash.com/photo-1574684891179-5d6c069ac4e0?w=400",
                "is_popular": False,
                "is_express": False
            },
            {
                "name": "🌹 Розы премиум",
                "category": "roses",
                "description": "Премиальные розы высшего качества. Для особых случаев.",
                "price": 1500000,  # 1,500,000 VND
                "photo_url": "https://images.unsplash.com/photo-1520763185298-1b434c919102?w=400",
                "is_popular": True,
                "is_express": True
            }
        ]
        
        # Добавляем товары в базу
        for product_data in products:
            product = Product(**product_data)
            db.add(product)
        
        db.commit()
        print(f"✅ Добавлено {len(products)} товаров")
        
        # Выводим статистику
        roses_count = db.query(Product).filter(Product.category == 'roses').count()
        exotic_count = db.query(Product).filter(Product.category == 'exotic').count()
        mix_count = db.query(Product).filter(Product.category == 'mix').count()
        mono_count = db.query(Product).filter(Product.category == 'mono').count()
        popular_count = db.query(Product).filter(Product.is_popular == True).count()
        
        print(f"\n📊 Статистика:")
        print(f"🌹 Розы: {roses_count}")
        print(f"🌺 Экзотика: {exotic_count}")
        print(f"💐 Микс: {mix_count}")
        print(f"🤍 Моно: {mono_count}")
        print(f"🔥 Популярные: {popular_count}")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_test_products()
