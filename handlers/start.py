from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from services.utils import delete_previous_message
from keyboards import KEYBOARD
from config import last_messages, user_states


router = Router()


@router.message(Command("start"))
async def start_message(message: Message):
    user_id = message.from_user.id
    await delete_previous_message(user_id)

    sent_message = await message.answer("Выберите действие:", reply_markup=KEYBOARD)

    last_messages[user_id] = sent_message.message_id
    user_states[user_id] = None
