import asyncio
from config import user_texts
from keyboards import BACK_BUTTON, KEYBOARD
from config import last_messages, user_states, sent_messages
from bot_istance import bot_tg as bot
from services.utils import delete_previous_message


async def send_saved_text(user_id: int):
    if user_id not in user_texts or not user_texts[user_id]:
        await delete_previous_message(user_id)
        sent_message = await bot.send_message(user_id, "У вас нет сохранённого текста.", reply_markup=BACK_BUTTON)
        last_messages[user_id] = sent_message.message_id
        return

    text = user_texts[user_id]
    words = text.split()
    sent_message = await bot.send_message(user_id, "Отправляю сохраненный текст по частям...")
    last_messages[user_id] = sent_message.message_id
    await asyncio.sleep(5)
    await delete_previous_message(user_id)

    sent_messages[user_id] = []
    for i in range(0, len(words), 5):
        if user_states.get(user_id) is True:
            await delete_previous_message(user_id)
            sent_message = await bot.send_message(user_id, "Бот остановлен.", reply_markup=KEYBOARD)
            last_messages[user_id] = sent_message.message_id
            user_states[user_id] = None
            return
        chunk = " ".join(words[i:i+5])
        await asyncio.sleep(10)
        sent_message = await bot.send_message(user_id, chunk)
        sent_messages[user_id].append(
            sent_message.message_id)
        await asyncio.sleep(10)

    await delete_previous_message(user_id)
    await asyncio.sleep(5)
    sent_message = await bot.send_message(user_id, "Весь текст отправлен.", reply_markup=BACK_BUTTON)
    last_messages[user_id] = sent_message.message_id
