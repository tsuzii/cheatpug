import os
from dotenv import load_dotenv
from aiogram import Bot

load_dotenv()
bot_tg = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
