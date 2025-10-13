"""
Скрипт для добавления тестовых товаров в базу данных
"""
import asyncio
import sys
import os

# Добавляем путь к backend
sys.path.append(os.path.join(os.path.dirname(__file__)))

from models.database import Product, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Подключение к БД
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/flowers')
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

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
            # Розы
            {
                "name": "🌹 Розы классические",
                "category": "roses",
                "description": "Красные розы в красивой упаковке. Идеально для романтических моментов.",
                "price": 800000,  # 800,000 VND
                "photo_url": "https://images.unsplash.com/photo-1518895949257-7621c3c786d7?w=400",
                "is_popular": True,
                "is_available": True
            },
            {
                "name": "🌹 Розы премиум",
                "category": "roses",
                "description": "Премиальные розы высшего качества. Для особых случаев.",
                "price": 1500000,  # 1,500,000 VND
                "photo_url": "https://images.unsplash.com/photo-1520763185298-1b434c919102?w=400",
                "is_popular": True,
                "is_available": True
            },
            {
                "name": "🌹 Розы белые",
                "category": "roses",
                "description": "Элегантные белые розы. Чистота и нежность.",
                "price": 900000,  # 900,000 VND
                "photo_url": "https://images.unsplash.com/photo-1574684891179-5d6c069ac4e0?w=400",
                "is_popular": False,
                "is_available": True
            },
            
            # Экзотика
            {
                "name": "🌺 Тропический рай",
                "category": "exotic",
                "description": "Экзотические цветы из тропиков. Яркие и необычные.",
                "price": 1200000,  # 1,200,000 VND
                "photo_url": "https://images.unsplash.com/photo-1563241527-3004b7be0ffd?w=400",
                "is_popular": True,
                "is_available": True
            },
            {
                "name": "🌺 Орхидеи фаленопсис",
                "category": "exotic",
                "description": "Красивые орхидеи в горшке. Долго будут радовать глаз.",
                "price": 1800000,  # 1,800,000 VND
                "photo_url": "https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=400",
                "is_popular": True,
                "is_available": True
            },
            {
                "name": "🌺 Антуриум красный",
                "category": "exotic",
                "description": "Яркий антуриум в горшке. Современный и стильный.",
                "price": 1400000,  # 1,400,000 VND
                "photo_url": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400",
                "is_popular": False,
                "is_available": True
            },
            
            # Микс
            {
                "name": "💐 Весенний микс",
                "category": "mix",
                "description": "Смесь весенних цветов разных оттенков. Свежесть и красота.",
                "price": 900000,  # 900,000 VND
                "photo_url": "https://images.unsplash.com/photo-1490750967868-88aa4486c946?w=400",
                "is_popular": True,
                "is_available": True
            },
            {
                "name": "💐 Романтический микс",
                "category": "mix",
                "description": "Нежный микс розовых и белых цветов. Для романтических моментов.",
                "price": 1100000,  # 1,100,000 VND
                "photo_url": "https://images.unsplash.com/photo-1513475382585-d06e58bcb0e0?w=400",
                "is_popular": True,
                "is_available": True
            },
            {
                "name": "💐 Яркий микс",
                "category": "mix",
                "description": "Яркий микс разноцветных цветов. Поднимет настроение!",
                "price": 950000,  # 950,000 VND
                "photo_url": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400",
                "is_popular": False,
                "is_available": True
            },
            
            # Моно
            {
                "name": "🤍 Белые лилии",
                "category": "mono",
                "description": "Элегантные белые лилии. Чистота и нежность.",
                "price": 700000,  # 700,000 VND
                "photo_url": "https://images.unsplash.com/photo-1574684891179-5d6c069ac4e0?w=400",
                "is_popular": False,
                "is_available": True
            },
            {
                "name": "💛 Желтые тюльпаны",
                "category": "mono",
                "description": "Яркие желтые тюльпаны. Весна и солнце!",
                "price": 600000,  # 600,000 VND
                "photo_url": "https://images.unsplash.com/photo-1520763185298-1b434c919102?w=400",
                "is_popular": True,
                "is_available": True
            },
            {
                "name": "💜 Фиолетовые ирисы",
                "category": "mono",
                "description": "Красивые фиолетовые ирисы. Загадочность и элегантность.",
                "price": 750000,  # 750,000 VND
                "photo_url": "https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=400",
                "is_popular": False,
                "is_available": True
            },
            
            # Дополнительные товары
            {
                "name": "🌻 Подсолнухи",
                "category": "mono",
                "description": "Яркие подсолнухи. Лето и радость!",
                "price": 550000,  # 550,000 VND
                "photo_url": "https://images.unsplash.com/photo-1597848212624-e19c8c6d0a6e?w=400",
                "is_popular": True,
                "is_available": True
            },
            {
                "name": "🌷 Тюльпаны микс",
                "category": "mix",
                "description": "Разноцветные тюльпаны. Весеннее настроение!",
                "price": 650000,  # 650,000 VND
                "photo_url": "https://images.unsplash.com/photo-1520763185298-1b434c919102?w=400",
                "is_popular": True,
                "is_available": True
            },
            {
                "name": "🌿 Зеленая композиция",
                "category": "exotic",
                "description": "Зеленая композиция из суккулентов. Современно и стильно.",
                "price": 850000,  # 850,000 VND
                "photo_url": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400",
                "is_popular": False,
                "is_available": True
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
