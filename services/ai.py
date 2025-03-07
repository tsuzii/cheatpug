import asyncio
import openai
import logging
import config

client = openai.OpenAI(
    api_key=config.DEEPSEEK_TOKEN,
    base_url=config.URL_DEEPSEEK
)


async def get_ai_response(prompt: str) -> str:
    try:
        full_response = ""

        response_stream = await asyncio.to_thread(
            client.chat.completions.create,
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )

        for chunk in response_stream:
            if chunk.choices[0].delta.content:
                content_piece = chunk.choices[0].delta.content
                full_response += content_piece

        return full_response.strip()

    except Exception as e:
        logging.error(f"Ошибка запроса к DeepSeek: {e}")
        return "Ошибка обработки запроса. Попробуйте позже."
