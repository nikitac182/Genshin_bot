from aiogram.filters import Command
from aiogram import types, Router, F
from config import ADMIN_ID
from consts import HELP_TEXT
from filters.ban_filter import IsNotBanned
from services.commands import admin_commands

router = Router()
router.message.filter(IsNotBanned())
router.callback_query.filter(IsNotBanned())

@router.message(F.from_user.id.in_(ADMIN_ID), Command("help"))
async def cmd_admin_help(message: types.Message):
    
    await message.answer(HELP_TEXT)

@router.message(F.from_user.id.in_(ADMIN_ID))
async def handler_admin_commands(message: types.Message):
    await admin_commands(message)