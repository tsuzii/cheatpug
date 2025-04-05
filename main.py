import asyncio
import logging
from bot_config import dp, shutdown
from bot_istance import bot_tg

# Настройка логирования: логируем и в файл, и в консоль
logging.basicConfig(
    level=logging.INFO,  # Уровень логирования (DEBUG, INFO, WARNING, ERROR)
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Вывод логов в консоль (stdout)
        logging.FileHandler("bot_logs.log")  # Запись логов в файл
    ],
)


async def main():
    logging.info("Бот запускается...")
    await bot_tg.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot_tg)
    except Exception as e:
        logging.error(f"Ошибка в боте: {e}", exc_info=True)
    finally:
        await shutdown()
        logging.info("Бот завершил работу.")

if __name__ == "__main__":
    asyncio.run(main())
