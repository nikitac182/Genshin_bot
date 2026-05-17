import asyncio
import aiogram
from aiogram.filters import CommandStart
from aiogram.types import *
from aiogram import Bot, Dispatcher, types, Router
from database import add_user
from keyboards.inline import menu_kb

router = Router()

@router.message(CommandStart())
async def start_command(message: types.Message):
    await add_user(message.from_user.id, message.from_user.username)
    await message.answer('Главное меню', reply_markup=menu_kb)
