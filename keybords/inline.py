import config
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Первая кнопка", callback_data="btn1")],
    [InlineKeyboardButton(text="Вторая кнопка", callback_data="btn2")],
    [InlineKeyboardButton(text="DEEPSEEK", callback_data="deepseek")]
])

subscription_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Подписаться на канал",
                          url=f"https://t.me/{config.CHANNEL_USERNAME}")],
    [InlineKeyboardButton(text="Проверить подписку",
                          callback_data="check_subscription")]
])
