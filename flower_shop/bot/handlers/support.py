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

# Убираем универсальный обработчик чтобы не мешать другим обработчикам
# @router.message() - этот обработчик перехватывал все сообщения!

