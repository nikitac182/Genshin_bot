from aiogram.types import *
from aiogram import Router
from keyboards.inline import menu_kb
from services.user_profile import set_story_wishes, set_profile

router = Router()

@router.callback_query(lambda c: c.data == 'profile')
async def handler_set_profile(call: CallbackQuery):
    await set_profile(call)

@router.callback_query(lambda c: c.data == 'story_wishes')
async def handler_set_story_wishes(call: CallbackQuery):
    await set_story_wishes(call)

@router.callback_query(lambda c: c.data == 'back_to_menu_from_profile')
async def back_to_menu_from_profile(call: CallbackQuery):
    await call.message.edit_text('Главное меню', reply_markup=menu_kb)
