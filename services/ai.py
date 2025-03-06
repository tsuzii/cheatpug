import asyncio
import openai
import logging
import config

client = openai.OpenAI(api_key=config.DEEPSEEK_TOKEN,
                       base_url=config.URL_DEEPSEEK)


async def get_ai_response(prompt: str) -> str:
    try:
        response = await asyncio.to_thread(  # Запускаем в отдельном потоке
            client.chat.completions.create,
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Ошибка запроса к DeepSeek: {e}")
        return "Ошибка обработки запроса. Попробуйте позже."
