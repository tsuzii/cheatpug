
from aiogram import Router
from bot_istance import bot_tg as bot
from aiogram.types import CallbackQuery
from services.utils import delete_previous_message
from services.subscription import check_subscription
from keyboards import SUB_KEYBOARD, KEYBOARD, BACK_BUTTON
from config import last_messages, user_states, sent_messages
from services.return_text import send_saved_text

router = Router()


@router.callback_query()
async def handle_buttons(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    sent_message = None

    if not await check_subscription(user_id):
        await delete_previous_message(user_id)
        sent_message = await callback_query.message.answer("Сначала подпишитесь на канал:", reply_markup=SUB_KEYBOARD)
        last_messages[user_id] = sent_message.message_id
        return

    await delete_previous_message(user_id)

    if callback_query.data == "check_subscription":
        if await check_subscription(user_id):
            sent_message = await callback_query.message.answer("Подписка подтверждена! Выберите действие:", reply_markup=KEYBOARD)
        else:
            sent_message = await callback_query.message.answer("Вы не подписаны! Подпишитесь и попробуйте снова:", reply_markup=SUB_KEYBOARD)

    if callback_query.data == "back":
        if user_id in sent_messages:
            for message_id in sent_messages[user_id]:
                try:
                    await bot.delete_message(user_id, message_id)
                except Exception:
                    pass
            sent_messages[user_id] = []
        user_states[user_id] = None
        sent_message = await callback_query.message.answer("Выберите действие:", reply_markup=KEYBOARD)

    elif callback_query.data == "deep_seek":
        sent_message = await callback_query.message.answer("Начни диалог с ChatGpt:", reply_markup=BACK_BUTTON)
        user_states[user_id] = "deep_seek"

    elif callback_query.data == "ai_request":
        sent_message = await callback_query.message.answer("Введите ваш вопрос для ChatGPT и я сохраню его для последующего отображения на браслете:", reply_markup=BACK_BUTTON)
        user_states[user_id] = "ai_request"

    elif callback_query.data == "add_text":
        sent_message = await callback_query.message.answer("Введите ваш текст одним сообщением и я сохраню его для последующего отображения на браслете:", reply_markup=BACK_BUTTON)
        user_states[user_id] = "add_text"

    elif callback_query.data == "show_saved_text":

        user_states[user_id] = "show_saved_text"
        await send_saved_text(user_id)

    if sent_message:
        last_messages[user_id] = sent_message.message_id
