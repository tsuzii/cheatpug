from aiogram import Dispatcher
from bot_istance import bot_tg
from handlers import router


dp = Dispatcher()

dp.include_router(router)


async def shutdown():
    """Функция для корректного закрытия бота"""
    await bot_tg.session.close()
