import asyncio
from operator import call
import aiogram
from aiogram.filters import CommandStart
from aiogram.types import *
from aiogram import Bot, Dispatcher, types, Router
from keyboards.inline import menu_kb, back_menu_kb
from database import *

router = Router()

@router.callback_query(lambda c: c.data == 'leaderboard')
async def set_leaderboard(call: CallbackQuery):
    caption = f'🏆 Топ игроков по круткам:'
    users = await get_users_for_leaderboard()
    for user in users:
        username, total_wishes = user
        caption += f'\n@{username} - {total_wishes} круток'
    await call.message.edit_text(caption, reply_markup=back_menu_kb)