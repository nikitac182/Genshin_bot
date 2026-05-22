from email.mime import message
from aiogram.filters import Command
from database import *
from aiogram import Bot, Dispatcher, types, Router
from services.commands import *
router = Router()

@router.message()
async def admin_commands_handler(message: types.Message):
    await admin_commands(message)
