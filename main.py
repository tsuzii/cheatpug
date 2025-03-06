import asyncio
import logging
from bot_config import dp, shutdown
from bot_istance import bot_tg


async def main():
    logging.basicConfig(level=logging.INFO)
    await bot_tg.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot_tg)

if __name__ == "__main__":
    asyncio.run(main())


async def main():
    logging.basicConfig(level=logging.INFO)
    await bot_tg.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot_tg)
    finally:
        await shutdown()
