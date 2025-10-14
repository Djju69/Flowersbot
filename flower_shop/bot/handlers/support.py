"""
Обработчики для поддержки клиентов
"""
import logging
from aiogram import Router, F
from aiogram.types import Message
import os

logger = logging.getLogger(__name__)
router = Router()

ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')

@router.message(F.text == "💬 Поддержка")
async def support_menu(message: Message):
    """Меню поддержки"""
    logger.info(f"💬 Запрос поддержки от {message.from_user.id}")
    
    await message.answer(
        "💬 <b>Поддержка клиентов</b>\n\n"
        "📞 Телефон: +84 XXX XXX XXX\n"
        "📧 Email: support@flowers-nhatrang.com\n"
        "🕐 Время работы: 8:00 - 22:00\n\n"
        "Или напишите ваш вопрос, и мы ответим в течение 15 минут!",
        parse_mode='HTML'
    )

@router.message()
async def forward_to_admin(message: Message):
    """Переслать сообщение админу"""
    # Проверяем что это не команда и не кнопка
    if message.text in ["🔁 Повторить", "📦 Мои заказы", "🔔 Напоминания", "💬 Поддержка"]:
        return
    
    # Проверяем что есть текст сообщения
    if not message.text:
        return
    
    logger.info(f"📨 Сообщение от {message.from_user.id} для поддержки: {message.text}")
    
    if ADMIN_CHAT_ID:
        try:
            # Пересылаем сообщение админу
            await message.forward(chat_id=int(ADMIN_CHAT_ID))
            
            # Отправляем подтверждение пользователю
            await message.answer(
                "✅ <b>Сообщение отправлено!</b>\n\n"
                "Мы получили ваш вопрос и ответим в течение 15 минут.",
                parse_mode='HTML'
            )
            
        except Exception as e:
            logger.error(f"Ошибка пересылки сообщения: {e}")
            await message.answer(
                "❌ <b>Ошибка</b>\n\n"
                "Не удалось отправить сообщение. Попробуйте позже или свяжитесь с нами по телефону.",
                parse_mode='HTML'
            )
    else:
        await message.answer(
            "❌ <b>Поддержка временно недоступна</b>\n\n"
            "Пожалуйста, свяжитесь с нами по телефону: +84 XXX XXX XXX",
            parse_mode='HTML'
        )
