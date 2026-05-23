import aiosqlite
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
    user_id = call.from_user.id
    users = await get_users_for_leaderboard()

    async with aiosqlite.connect('sqlite.db') as db:
        async with db.execute('SELECT COUNT(*) FROM users') as cursor:
            total_users = await cursor.fetchone()
            total_users = total_users[0] if total_users else 0
        async with db.execute(
            'SELECT COUNT(*) + 1 FROM users WHERE total_wishes > (SELECT total_wishes FROM users WHERE user_id = ?)',
            (user_id,)
        ) as cursor:
            position = await cursor.fetchone()
            position = position[0] if position else '?'

    caption = f'🏆 Топ игроков по круткам:\n'
    i = 1
    for user in users:
        name, username, uid, total_wishes = user
        username = f'@{username}'
        text = f'<a href="tg://user?id={uid}">{username if username else name}</a>'
        caption += f'\n{i}. {text} - {total_wishes} круток'
        i += 1
    caption += f'═══════════════\n📊 Ваша позиция: {position}/{total_users}'
    await call.message.edit_text(caption, reply_markup=back_menu_kb, parse_mode='HTML')