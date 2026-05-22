from operator import call
from aiogram.types import *
from aiogram import  Router
from filters.ban_filter import IsNotBanned
from keyboards.inline import back_menu_kb
from database import *

router = Router()
router.message.filter(IsNotBanned())
router.callback_query.filter(IsNotBanned())


@router.callback_query(lambda c: c.data == 'leaderboard')
async def set_leaderboard(call: CallbackQuery):
    caption = f'🏆 Топ игроков по круткам:'
    users = await get_users_for_leaderboard()
    for user in users:
        name, username, user_id, total_wishes = user
        username = f'@{username}'
        text = f'<a href="tg://user?id={user_id}">{username if username else name}</a>'
        caption += f'\n{text} - {total_wishes} круток'
    await call.message.edit_text(caption, reply_markup=back_menu_kb, parse_mode='HTML')