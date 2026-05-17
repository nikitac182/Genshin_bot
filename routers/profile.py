import asyncio
from operator import call
import aiogram
from aiogram.filters import CommandStart
from aiogram.types import *
from aiogram import Bot, Dispatcher, types, Router
from keyboards.inline import menu_kb, back_menu_kb
from database import *

router = Router()

@router.callback_query(lambda c: c.data == 'profile')
async def set_profile(call: CallbackQuery):

    primogems = await get_primogems(call.from_user.id)
    total_wishes = await get_total_wishes(call.from_user.id)
    stardust = await get_stardust(call.from_user.id)
    starglitter = await get_starglitter(call.from_user.id)
    characters_list = None
    weapons_list = None
    caption = f'''
👤 Ваш профиль:

💎 Примогемов: {primogems}
🎲 Всего круток: {total_wishes}
✨ Звёздная пыль: {stardust}
⭐️ Звёздный блеск: {starglitter}

💫 Список персонажей (с созвездиями):
{characters_list}

🗡 Выбито оружий 4★/5★:
{weapons_list}
'''
    await call.message.edit_text(caption, reply_markup=back_menu_kb)

@router.callback_query(lambda c: c.data == 'back_to_menu_from_profile')
async def back_to_menu_from_profile(call: CallbackQuery):
    await call.message.edit_text('Главное меню', reply_markup=menu_kb)

