from aiogram.filters import CommandStart
from aiogram import types, Router, F
from database import add_user, get_status
from filters.ban_filter import IsNotBanned
from keyboards.inline import menu_kb, group_menu_kb
from datetime import datetime
import aiosqlite

router = Router()
router.message.filter(IsNotBanned(), F.chat.type.in_({"group", "supergroup"}))

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
    await message.reply(
        f'Главное меню пользователя {message.from_user.username}',
        reply_markup=group_menu_kb(message.from_user.id)
    )
