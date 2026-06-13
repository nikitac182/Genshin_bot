from aiogram import Router
from aiogram.types import CallbackQuery
from services.gacha import wish_one_time, wish_ten_times
from filters.ban_filter import IsNotBanned
from database import get_primogems

router = Router()
router.message.filter(IsNotBanned())
router.callback_query.filter(IsNotBanned())


@router.callback_query(lambda c: c.data.startswith('wish_10'))
async def wish_10_handler(call: CallbackQuery):
    if len(call.data.split('_')) == 3 and int(call.from_user.id) != int(call.data.split('_')[2]):
        call.answer()
        return
    primogems = await get_primogems(call.from_user.id)
    if primogems < 1600:
        await call.answer("❌ Недостаточно примогемов!", show_alert=True, cache_time=1)
        return
    await call.answer(cache_time=1)
    await wish_ten_times(call.from_user.id, call)

@router.callback_query(lambda c: c.data.startswith('wish_1'))
async def wish_1_handler(call: CallbackQuery):
    if len(call.data.split('_')) == 3 and int(call.from_user.id) != int(call.data.split('_')[2]):
        call.answer()
        return
    primogems = await get_primogems(call.from_user.id)
    if primogems < 160:
        await call.answer("❌ Недостаточно примогемов!", show_alert=True, cache_time=1)
        return
    await call.answer(cache_time=1)
    await wish_one_time(call.from_user.id, call)


