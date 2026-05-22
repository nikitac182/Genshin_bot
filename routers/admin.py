from aiogram.filters import Command
from aiogram import types, Router, F
from config import ADMIN_ID

router = Router()


@router.message(F.from_user.id.in_(ADMIN_ID), Command("help"))
async def cmd_admin_help(message: types.Message):
    help_text = """
    🛡️ Админ команды:
    /add_primogems <user_id> <amount> - Добавить примогемы
    /reduce_primogems <user_id> <amount> - Уменьшить примогемы
    /ban <user_id> <hours> - Забанить пользователя
    /unban <user_id> - Разбанить пользователя
    /delete_user <user_id> - Удалить пользователя
    /get_user <user_id> - Информация о пользователе
    """
    await message.answer(help_text)