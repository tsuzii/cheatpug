import tokens
import logging
import openai
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message

# Укажите токены
TELEGRAM_BOT_TOKEN = tokens.TELEGRAM_BOT_TOKEN
DEEPSEEK_API_KEY = tokens.DEEPSEEK_TOKEN

# Настройки OpenAI (DeepSeek совместим с OpenAI API)
client = openai.OpenAI(api_key=DEEPSEEK_API_KEY,
                       base_url="https://api.deepseek.com")

# Создаем бот и диспетчер
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()


async def get_ai_response(prompt: str) -> str:
    """Получает ответ от DeepSeek API."""
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",  # Или другая модель DeepSeek
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Ошибка запроса к DeepSeek: {e}")
        return "Ошибка обработки запроса. Попробуйте позже."


@dp.message()
async def handle_message(message: Message):
    """Обрабатывает входящие сообщения."""
    response = await get_ai_response(message.text)
    await message.answer(response)


async def main():
    """Запуск бота."""
    logging.basicConfig(level=logging.INFO)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
