import config
from bot_istance import bot_tg as bot


async def check_subscription(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(f"@{config.CHANNEL_USERNAME}", user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        print(f"Ошибка проверки подписки: {e}")
        return False
