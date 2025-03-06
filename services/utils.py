import logging
from config import last_messages
from bot_istance import bot_tg as bot


async def delete_previous_message(user_id: int):
    """Удаляет предыдущее сообщение пользователя, если оно есть в last_messages."""
    if user_id in last_messages:
        try:
            await bot.delete_message(chat_id=user_id, message_id=last_messages[user_id])
            del last_messages[user_id]  # Удаляем сообщение из памяти
        except Exception as e:
            logging.warning(
                f"Не удалось удалить предыдущее сообщение пользователя {user_id}: {e}")
