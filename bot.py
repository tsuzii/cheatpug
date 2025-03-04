import config
import openai
import asyncio
import logging
from aiogram.filters import Command
from aiogram import Bot, Dispatcher, F
from config import last_messages, user_states, user_texts, saved_texts
from keyboards.inline import subscription_keyboard, keyboard, BACK_BUTTON
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

client = openai.OpenAI(api_key=config.DEEPSEEK_TOKEN,
                       base_url=config.URL_DEEPSEEK)

bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()


async def check_subscription(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(f"@{config.CHANNEL_USERNAME}", user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        logging.error(f"Ошибка при проверке подписки: {e}")
        return False


async def get_ai_response(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Ошибка запроса к DeepSeek: {e}")
        return "Ошибка обработки запроса. Попробуйте позже."


async def delete_previous_message(user_id: int):
    if user_id in last_messages:
        try:
            await bot.delete_message(chat_id=user_id, message_id=last_messages[user_id])
        except Exception as e:
            logging.warning(f"Не удалось удалить предыдущее сообщение: {e}")


async def send_saved_text(user_id: int):
    """Отправляет сохранённый текст пользователю частями по 2-3 слова с задержкой 5 секунд."""
    if user_id not in user_texts or not user_texts[user_id]:
        await bot.send_message(user_id, "У вас нет сохранённого текста.")
        return

    text = user_texts[user_id]  # Берём сохранённый текст пользователя
    words = text.split()  # Разбиваем на слова

    # Отправляем текст частями (по 2-3 слова)
    for i in range(0, len(words), 5):
        await asyncio.sleep(10)  # Шаг = 2 слова
        chunk = " ".join(words[i:i+5])  # Берём 2-3 слова
        await bot.send_message(user_id, chunk)
        # Пауза 5 секунд между отправками


@dp.message(Command("start"))
async def start_message(message: Message):
    user_id = message.from_user.id
    await delete_previous_message(user_id)

    if not await check_subscription(user_id):
        sent_message = await message.answer("Для доступа к боту подпишитесь на канал:", reply_markup=subscription_keyboard)
    else:
        sent_message = await message.answer("Выберите действие:", reply_markup=keyboard)

    last_messages[user_id] = sent_message.message_id
    user_states[user_id] = None


@dp.message()
async def handle_all_messages(message: Message):
    """Обработчик всех входящих сообщений, с проверкой подписки."""
    user_id = message.from_user.id

    # Проверяем подписку перед любым ответом
    if not await check_subscription(user_id):
        sent_message = await message.answer("Сначала подпишитесь на канал:", reply_markup=subscription_keyboard)
        last_messages[user_id] = sent_message.message_id
        return  # Прекращаем выполнение

    await delete_previous_message(user_id)

    # Проверяем состояние пользователя
    if user_states.get(user_id) == "deep_seek":
        response = await get_ai_response(message.text)
        sent_message = await message.answer(response, reply_markup=BACK_BUTTON)

    elif user_states.get(user_id) == "ai_request":
        response = await get_ai_response(message.text)
        user_texts[user_id] = response
        sent_message = await message.answer("Ваш запрос обработан.", reply_markup=BACK_BUTTON)

    elif user_states.get(user_id) == "add_text":
        # Просто сохраняем текст (например, в БД или файл)
        user_texts[user_id] = message.text
        sent_message = await message.answer("Текст сохранён.", reply_markup=BACK_BUTTON)

    else:
        sent_message = await message.answer("Я не понял команду. Выберите действие в меню:", reply_markup=keyboard)

    last_messages[user_id] = sent_message.message_id


@dp.callback_query()
async def handle_buttons(callback_query: CallbackQuery):
    """Обработчик всех кнопок, с проверкой подписки."""
    user_id = callback_query.from_user.id

    # Проверяем подписку перед выполнением любой кнопки
    if not await check_subscription(user_id):
        sent_message = await callback_query.message.answer("Сначала подпишитесь на канал:", reply_markup=subscription_keyboard)
        last_messages[user_id] = sent_message.message_id
        return  # Прекращаем выполнение

    await delete_previous_message(user_id)

    sent_message = None  # Переменная по умолчанию

    if callback_query.data == "check_subscription":
        if await check_subscription(user_id):
            sent_message = await callback_query.message.answer("Подписка подтверждена! Выберите действие:", reply_markup=keyboard)
        else:
            sent_message = await callback_query.message.answer("Вы не подписаны! Подпишитесь и попробуйте снова:", reply_markup=subscription_keyboard)

    elif callback_query.data == "back":
        sent_message = await callback_query.message.answer("Выберите действие:", reply_markup=keyboard)
        user_states[user_id] = None

    elif callback_query.data == "deep_seek":
        sent_message = await callback_query.message.answer("Введите ваш вопрос для DeepSeek:", reply_markup=BACK_BUTTON)
        user_states[user_id] = "deep_seek"

    elif callback_query.data == "ai_request":
        sent_message = await callback_query.message.answer("Введите ваш запрос для AI:", reply_markup=BACK_BUTTON)
        user_states[user_id] = "ai_request"

    elif callback_query.data == "add_text":
        sent_message = await callback_query.message.answer("Введите ваш текст для сохранения:", reply_markup=BACK_BUTTON)
        user_states[user_id] = "add_text"

    elif callback_query.data == "show_saved_text":
        asyncio.create_task(send_saved_text(user_id))  # Запускаем в фоне
        sent_message = await callback_query.message.answer("Отправляю ваш текст по частям...")

    if sent_message:
        last_messages[user_id] = sent_message.message_id
    else:
        logging.warning(
            f"Не удалось обработать callback_data: {callback_query.data}")


@dp.message(F.text)
async def handle_message(message: Message):
    user_id = message.from_user.id
    await delete_previous_message(user_id)

    if not await check_subscription(user_id):
        sent_message = await message.answer("Сначала подпишитесь на канал:", reply_markup=subscription_keyboard)

    elif user_states.get(user_id) == "deep_seek":
        response = await get_ai_response(message.text)
        sent_message = await message.answer(response, reply_markup=BACK_BUTTON)

    elif user_states.get(user_id) == "ai_request":
        # AI обработает, но ответ не показываем
        await get_ai_response(message.text)
        sent_message = await message.answer("Запрос обработан. Возвращаю в меню.", reply_markup=keyboard)

    elif user_states.get(user_id) == "add_text":
        saved_texts[user_id] = message.text
        sent_message = await message.answer("Текст сохранен. Возвращаю в меню.", reply_markup=keyboard)

    else:
        sent_message = await message.answer("Выберите действие:", reply_markup=keyboard)

    last_messages[user_id] = sent_message.message_id


async def main():
    logging.basicConfig(level=logging.INFO)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
