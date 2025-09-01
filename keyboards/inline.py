import os
from dotenv import load_dotenv
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

load_dotenv()

KEYBOARD = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="ChatGPT", callback_data="deep_seek")],
    [InlineKeyboardButton(text="Спросить и сохранить",
                          callback_data="ai_request")],
    [InlineKeyboardButton(text="Добавить текст вручную",
                          callback_data="add_text")],
    [InlineKeyboardButton(text="Вывод текста",
                          callback_data="show_saved_text")]
])


BACK_BUTTON = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Назад в меню", callback_data="back")]])
