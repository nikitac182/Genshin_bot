from aiogram import Router
from aiogram.types import CallbackQuery
from services.gacha import wish_one_time, wish_ten_times
from filters.ban_filter import IsNotBanned
from database import *

router = Router()
router.message.filter(IsNotBanned())
router.callback_query.filter(IsNotBanned())


@router.callback_query(lambda c: c.data == 'wish_1')
async def wish_1_handler(call: CallbackQuery):
    if int(call.from_user.id) != int(call.data.split('_')[2]):
        call.answer()
        return
    await wish_one_time(call.from_user.id, call)


@router.callback_query(lambda c: c.data == 'wish_10')
async def wish_10_handler(call: CallbackQuery):
    if int(call.from_user.id) != int(call.data.split('_')[2]):
        call.answer()
        return
    await wish_ten_times(call.from_user.id, call)