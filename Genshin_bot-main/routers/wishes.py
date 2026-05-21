import asyncio
import aiogram
from aiogram.filters import CommandStart
from aiogram.types import *
from aiogram import Bot, Dispatcher, types, Router
from keyboards.inline import menu_kb
from database import *
from services.gacha import wish_one_time, wish_ten_times

router = Router()

@router.callback_query(lambda c: c.data == 'wish_1')
async def some_command(call: CallbackQuery):
    user_id = call.from_user.id
    await wish_one_time(user_id, call)


@router.callback_query(lambda c: c.data == 'wish_10')
async def some_command(call: CallbackQuery):
    user_id = call.from_user.id
    await wish_ten_times(user_id, call)