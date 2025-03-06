from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from services.utils import delete_previous_message
from services.subscription import check_subscription
from keyboards import SUB_KEYBOARD, KEYBOARD
from config import last_messages, user_states


router = Router()


@router.message(Command("start"))
async def start_message(message: Message):
    user_id = message.from_user.id
    await delete_previous_message(user_id)

    if not await check_subscription(user_id):
        sent_message = await message.answer("Для доступа к боту подпишитесь на канал:", reply_markup=SUB_KEYBOARD)
    else:
        sent_message = await message.answer("Выберите действие:", reply_markup=KEYBOARD)

    last_messages[user_id] = sent_message.message_id
    user_states[user_id] = None
