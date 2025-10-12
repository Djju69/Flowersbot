"""
Утилиты для отправки уведомлений в Telegram Bot
"""
import aiohttp
import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

async def send_order_notification(order_id: int, order_data: Dict[str, Any]):
    """Отправить уведомление о новом заказе в Telegram Bot"""
    
    try:
        # Получаем токен бота и ID админа
        bot_token = os.getenv('BOT_TOKEN')
        admin_chat_id = os.getenv('ADMIN_CHAT_ID')
        
        if not bot_token or not admin_chat_id:
            logger.warning("BOT_TOKEN или ADMIN_CHAT_ID не настроены")
            return
        
        # Форматируем сообщение
        message = format_order_message(order_id, order_data)
        
        # Отправляем сообщение
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {
            'chat_id': admin_chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                if response.status == 200:
                    logger.info(f"✅ Уведомление о заказе #{order_id} отправлено")
                else:
                    logger.error(f"❌ Ошибка отправки уведомления: {response.status}")
                    
    except Exception as e:
        logger.error(f"❌ Ошибка отправки уведомления: {e}")

def format_order_message(order_id: int, order_data: Dict[str, Any]) -> str:
    """Форматировать сообщение о заказе"""
    
    # Форматируем цену в VND
    def format_price(price: int) -> str:
        return f"{price:,} ₫".replace(',', ' ')
    
    # Определяем тип контакта
    contact_type_map = {
        'telegram': '📱 Telegram',
        'whatsapp': '💬 WhatsApp', 
        'zalo': '💙 Zalo'
    }
    
    contact_type = contact_type_map.get(order_data.get('contact_type', ''), '📱 Контакт')
    
    message = f"""🆕 <b>Новый заказ #{order_id}</b>

👤 <b>Заказчик:</b> {order_data.get('name', 'Не указано')}
📱 <b>Telegram:</b> @{order_data.get('telegram_username', 'Не указано')}

🎁 <b>Получатель:</b> {order_data.get('recipient_name', 'Не указано')}
{contact_type}: {order_data.get('contact_value', 'Не указано')}

📍 <b>Доставка:</b>
• Координаты: {order_data.get('latitude', 'Не указано')}, {order_data.get('longitude', 'Не указано')}
• Адрес: {order_data.get('address_text', 'Не указано')}
• Дата: {order_data.get('delivery_date', 'Не указано')}
• Время: {order_data.get('delivery_time', 'Не указано')}

💌 <b>Открытка:</b> {order_data.get('card_text', 'Нет')}
🎭 <b>Анонимно:</b> {'Да' if order_data.get('is_anonymous') else 'Нет'}

💰 <b>Сумма:</b>
• Товары: {format_price(order_data.get('items_total', 0))}
• Доставка: {format_price(order_data.get('delivery_cost', 0))}
• <b>Итого: {format_price(order_data.get('total', 0))}</b>

📦 <b>Товары:</b>"""
    
    # Добавляем товары
    for item in order_data.get('items', []):
        message += f"\n• {item.get('product_name', 'Товар')} ({item.get('size', 'стандарт')}) - {format_price(item.get('price', 0))} x {item.get('quantity', 1)}"
    
    return message
