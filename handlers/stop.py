from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from services.utils import delete_previous_message
from config import last_messages, user_states
from keyboards import KEYBOARD

router = Router()


@router.message(Command("stop"))
async def stop_message(message: Message):
    user_id = message.from_user.id
    await delete_previous_message(user_id)

    # Сброс состояния пользователя
    user_states[user_id] = True
