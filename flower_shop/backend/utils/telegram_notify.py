"""
Утилиты для отправки уведомлений в Telegram
"""
import aiohttp
import os
import logging

logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')

async def send_telegram_message(chat_id: int, text: str):
    """Отправить сообщение в Telegram"""
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN не найден")
        return
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json={
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "HTML"
            }) as response:
                if response.status == 200:
                    logger.info(f"Сообщение отправлено в чат {chat_id}")
                else:
                    logger.error(f"Ошибка отправки сообщения: {response.status}")
        except Exception as e:
            logger.error(f"Ошибка отправки сообщения: {e}")

async def send_order_notification(order_id: int, order_data: dict):
    """Отправить уведомление о заказе"""
    
    # Уведомление админу
    admin_text = f"""🆕 <b>Новый заказ #{order_id}</b>

👤 <b>Клиент:</b> {order_data['name']}
📞 <b>Телефон:</b> {order_data['phone']}
📍 <b>Адрес:</b> {order_data['address']}
📅 <b>Дата:</b> {order_data['delivery_date']}
⏰ <b>Время:</b> {order_data['delivery_time']}

💰 <b>Сумма:</b> {order_data['total']:,} VND

<b>Товары:</b>
"""
    
    for item in order_data['items']:
        admin_text += f"• {item['product_name']} ({item['size']}) x{item['quantity']} - {item['price']:,} VND\n"
    
    if order_data.get('card_text'):
        admin_text += f"\n💌 <b>Открытка:</b> {order_data['card_text']}"
    
    await send_telegram_message(int(ADMIN_CHAT_ID), admin_text)
    
    # Уведомление клиенту
    client_text = f"""✅ <b>Заказ #{order_id} принят!</b>

Спасибо за заказ! Мы свяжемся с вами для подтверждения деталей.

📅 <b>Доставка:</b> {order_data['delivery_date']} в {order_data['delivery_time']}
💰 <b>Сумма:</b> {order_data['total']:,} VND

<b>Статус:</b> Ожидаем подтверждения"""
    
    await send_telegram_message(order_data['telegram_id'], client_text)

async def send_status_update(telegram_id: int, order_id: int, status: str):
    """Отправить обновление статуса заказа"""
    
    status_texts = {
        'confirmed': '✅ Заказ подтвержден! Начинаем сборку букета.',
        'making': '🌸 Ваш букет собирается! Скоро будет готов.',
        'delivering': '🚚 Ваш букет в пути! Курьер уже едет к вам.',
        'delivered': '🎉 Заказ доставлен! Надеемся, вам понравилось!',
        'cancelled': '❌ Заказ отменен. Если у вас есть вопросы, обращайтесь в поддержку.'
    }
    
    text = f"""📦 <b>Заказ #{order_id}</b>

{status_texts.get(status, f'Статус изменен на: {status}')}"""
    
    await send_telegram_message(telegram_id, text)
