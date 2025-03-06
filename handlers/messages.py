import random
from aiogram import Router
from aiogram.types import Message
from services.ai import get_ai_response
from services.utils import delete_previous_message
from services.subscription import check_subscription
from keyboards import BACK_BUTTON, KEYBOARD, SUB_KEYBOARD
from config import user_states, user_texts, last_messages, rand_answers

router = Router()


@router.message()
async def handle_all_messages(message: Message):
    user_id = message.from_user.id
    sent_message = None

    if not await check_subscription(user_id):
        sent_message = await message.answer("Сначала подпишитесь на канал:", reply_markup=SUB_KEYBOARD)
        last_messages[user_id] = sent_message.message_id
        return

    await delete_previous_message(user_id)

    if user_states.get(user_id) == "deep_seek":
        sent_message = await message.answer(random.choice(rand_answers))
        last_messages[user_id] = sent_message.message_id
        response = await get_ai_response(message.text)
        await delete_previous_message(user_id)
        sent_message = await message.answer(response, reply_markup=BACK_BUTTON)

    elif user_states.get(user_id) == "ai_request":
        sent_message = await message.answer(random.choice(rand_answers))
        last_messages[user_id] = sent_message.message_id
        response = await get_ai_response(message.text)
        user_texts[user_id] = response
        await delete_previous_message(user_id)
        sent_message = await message.answer("Ваш запрос обработан. ", reply_markup=BACK_BUTTON)

    elif user_states.get(user_id) == "add_text":
        user_texts[user_id] = message.text
        sent_message = await message.answer("Текст сохранён.", reply_markup=BACK_BUTTON)

    else:
        sent_message = await message.answer("Я не понял команду. Выберите действие:", reply_markup=KEYBOARD)

    if sent_message:
        last_messages[user_id] = sent_message.message_id
