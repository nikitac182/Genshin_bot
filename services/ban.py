from aiogram.types import Message
from database import update_user_ban_status, delete_user


async def ban_user(message: Message, user_id: int, duration: int):
    await update_user_ban_status(
        user_id,
        is_banned=True,
        ban_end_time=duration
    )
    await delete_user(user_id)
    await message.answer(
        f"Пользователь с ID {user_id} был забанен на {duration} часов."
    )


async def unban_user(message: Message, user_id: int):
    await update_user_ban_status(
        user_id,
        is_banned=False
    )
    await message.answer(
        f"Пользователь с ID {user_id} был разбанен."
    )