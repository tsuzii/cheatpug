from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from services.utils import delete_previous_message
from config import user_states, last_messages


router = Router()


@router.message(Command("stop"))
async def stop_message(message: Message):
    user_id = message.from_user.id
    await delete_previous_message(user_id)
    user_states[user_id] = True
    sent_message = await message.answer("Ожидайте остановки процесса.")
    last_messages[user_id] = sent_message.message_id
