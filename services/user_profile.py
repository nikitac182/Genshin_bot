from aiogram.types import CallbackQuery, Message
from config import ADMIN_ID, ADMIN_USERNAME
from aiogram.fsm.context import FSMContext
from consts import CONTACT_ADMIN_MESSAGE, PROFILE_CAPTION
from keyboards.inline import *
from database import *


async def set_story_wishes(call: CallbackQuery):
    wishes = await data_wishes(call.from_user.id)
    caption = '📜 История круток:\n\n'
    if not wishes:
        caption = "📜 История круток пуста."
    else:
        for wish in wishes:
            item_name, rarity, timestamp = wish
            caption += f'''
═══════════════
Вы получили:

{'⭐'*rarity} {item_name}

**Баннер:** {None}
✨ **Получено:**{None}
время: {timestamp}

'''
    
    await call.message.edit_text(caption, reply_markup=wish_menu_kb, parse_mode='HTML')

async def set_profile(call: CallbackQuery):

    primogems = await get_primogems(call.from_user.id)
    total_wishes = await get_total_wishes(call.from_user.id)
    stardust = await get_stardust(call.from_user.id)
    starglitter = await get_starglitter(call.from_user.id)
    characters_list = await get_characters(call.from_user.id)
    weapons_list = await get_weapons(call.from_user.id)
    caption = PROFILE_CAPTION.format(
        primogems=primogems,
        total_wishes=total_wishes,
        stardust=stardust,
        starglitter=starglitter,
        characters_list="\n-".join(characters_list),
        weapons_list="\n-".join(weapons_list)
    )
    await call.message.edit_text(caption, reply_markup=profile_kb)