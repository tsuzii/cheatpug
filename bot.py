import tokens
import logging
import openai
import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

CHANNEL_USERNAME="***REMOVED***"

client = openai.OpenAI(api_key=tokens.DEEPSEEK_TOKEN,
                       base_url="https://api.deepseek.com")


bot = Bot(token=tokens.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()
last_messages = {}

keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Первая кнопка", callback_data="btn1")],
    [InlineKeyboardButton(text="Вторая кнопка", callback_data="btn2")],
    [InlineKeyboardButton(text="DEEPSEEK", callback_data="deepseek")]
])

subscription_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Подписаться на канал",
                          url=f"https://t.me/{CHANNEL_USERNAME}")],
    [InlineKeyboardButton(text="Проверить подписку",
                          callback_data="check_subscription")]
])


async def check_subscription(user_id: int) -> bool:
    """Проверяет подписку пользователя на канал."""
    try:
        member = await bot.get_chat_member(f"@{CHANNEL_USERNAME}", user_id)

        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        logging.error(f"Ошибка при проверке подписки: {e}")
        return False


async def get_ai_response(prompt: str) -> str:
    """Получает ответ от DeepSeek API."""
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
    """Удаляет предыдущее сообщение от бота пользователю, если оно есть."""
    if user_id in last_messages:
        try:
            await bot.delete_message(chat_id=user_id, message_id=last_messages[user_id])
        except Exception as e:
            logging.warning(f"Не удалось удалить предыдущее сообщение: {e}")


@dp.message()
async def start_message(message: Message):
    """Проверяет подписку и отправляет клавиатуру."""
    user_id = message.from_user.id
    await delete_previous_message(user_id)

    if not await check_subscription(user_id):
        sent_message = await message.answer("Для доступа к боту подпишитесь на канал:", reply_markup=subscription_keyboard)
    else:
        sent_message = await message.answer("Выберите действие:", reply_markup=keyboard)

    last_messages[user_id] = sent_message.message_id


@dp.callback_query()
async def handle_buttons(callback_query: types.CallbackQuery):
    """Обрабатывает нажатия кнопок."""
    user_id = callback_query.from_user.id
    await delete_previous_message(user_id)

    if callback_query.data == "check_subscription":
        if await check_subscription(user_id):
            sent_message = await callback_query.message.answer("Подписка подтверждена! Выберите действие:", reply_markup=keyboard)
        else:
            sent_message = await callback_query.message.answer("Вы не подписаны! Подпишитесь и попробуйте снова:", reply_markup=subscription_keyboard)
        last_messages[user_id] = sent_message.message_id
        return

    if not await check_subscription(user_id):
        sent_message = await callback_query.message.answer("Сначала подпишитесь на канал:", reply_markup=subscription_keyboard)
        last_messages[user_id] = sent_message.message_id
        return

    if callback_query.data == "deepseek":
        sent_message = await callback_query.message.answer("Введите ваш вопрос для DeepSeek:")
    else:
        await callback_query.answer(f"Вы нажали: {callback_query.data}", show_alert=True)
        return

    last_messages[user_id] = sent_message.message_id


@dp.message()
async def handle_message(message: Message):
    """Обрабатывает входящие сообщения только после нажатия DeepSeek."""
    user_id = message.from_user.id
    await delete_previous_message(user_id)

    if not await check_subscription(user_id):
        sent_message = await message.answer("Сначала подпишитесь на канал:", reply_markup=subscription_keyboard)
    else:
        response = await get_ai_response(message.text)
        sent_message = await message.answer(response)

    last_messages[user_id] = sent_message.message_id


async def main():
    """Запуск бота."""
    logging.basicConfig(level=logging.INFO)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
