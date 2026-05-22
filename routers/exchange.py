from aiogram import Router
from aiogram.types import CallbackQuery
from filters.ban_filter import IsNotBanned
from keyboards.inline import menu_kb
from database import get_stardust, get_starglitter, get_primogems
import aiosqlite

router = Router()
router.message.filter(IsNotBanned())


@router.callback_query(lambda c: c.data == 'exchange')
async def exchange_stuff(call: CallbackQuery):
    user_id = call.from_user.id
    
    stardust = await get_stardust(user_id)
    starglitter = await get_starglitter(user_id)
    
    dust_used = (stardust // 75) * 75
    glitter_used = (starglitter // 5) * 5
    
    if dust_used == 0 and glitter_used == 0:
        await call.answer(
            "❌ Недостаточно ресурсов для обмена!\n\n"
            "Нужно: 75 звёздной пыли или 5 звёздного блеска",
            show_alert=True
        )
        return
    
    gems_from_dust = (dust_used // 75) * 160
    gems_from_glitter = (glitter_used // 5) * 160
    total_gems = gems_from_dust + gems_from_glitter
    
    async with aiosqlite.connect('sqlite.db') as db:
        await db.execute(
            'UPDATE users SET stardust = stardust - ?, starglitter = starglitter - ?, primogems = primogems + ? WHERE user_id = ?',
            (dust_used, glitter_used, total_gems, user_id)
        )
        await db.commit()

    new_primogems = await get_primogems(user_id)
    
    msg = (
        f"✨ **Обмен завершён!**\n\n"
        f"💎 **Новый баланс:** {new_primogems}\n\n"
    )
    
    await call.message.answer(msg, parse_mode="Markdown", reply_markup=menu_kb)
    await call.answer()