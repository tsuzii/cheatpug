import config
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

KEYBOARD = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="ChatGPT", callback_data="deep_seek")],
    [InlineKeyboardButton(text="Спросить и сохранить",
                          callback_data="ai_request")],
    [InlineKeyboardButton(text="Добавить текст вручную",
                          callback_data="add_text")],
    [InlineKeyboardButton(text="Вывод текста",
                          callback_data="show_saved_text")]
])

SUB_KEYBOARD = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Подписаться на канал",
                          url=f"https://t.me/{config.CHANNEL_USERNAME}")],
    [InlineKeyboardButton(text="Проверить подписку",
                          callback_data="check_subscription")]
])

BACK_BUTTON = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Назад в меню", callback_data="back")]])
