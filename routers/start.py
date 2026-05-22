from aiogram.filters import CommandStart
from aiogram import types, Router
from database import add_user, get_status
from filters.ban_filter import IsNotBanned
from keyboards.inline import menu_kb
from datetime import datetime
import aiosqlite

router = Router()
router.message.filter(IsNotBanned())

@router.message(CommandStart())
async def start_command(message: types.Message):
    if await get_status(message.from_user.id) == 'banned':
        await message.answer("Вы заблокированы.")
        return
    
    await add_user(message.from_user.id, message.from_user.username, message.from_user.full_name)
    async with aiosqlite.connect('sqlite.db') as db:
        await db.execute(
            'UPDATE users SET hour_reward = ? WHERE user_id = ?',
            (datetime.now(), message.from_user.id)
        )
        await db.commit()
    await message.answer('Главное меню', reply_markup=menu_kb)
