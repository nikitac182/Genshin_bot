from aiogram.types import CallbackQuery
from database import update_user_ban_status

async def ban_user(call: CallbackQuery, user_id: int, duration: int):
    await update_user_ban_status(user_id, is_banned=True, ban_end_time=duration)
    await call.message.answer(f"Пользователь с ID {user_id} был забанен на {duration} часов.")

async def unban_user(call: CallbackQuery, user_id: int):
    await update_user_ban_status(user_id, is_banned=False)
    await call.message.answer(f"Пользователь с ID {user_id} был разбанен.")