from aiogram.filters import Command
from database import *
from aiogram import types, Router, F
from services.ban import ban_user, unban_user
from config import ADMIN_ID

router = Router()

@router.message(F.from_user.id.in_(ADMIN_ID))
async def admin_commands(message: types.Message):
    if message.text == '/start' or not message.text:
        return
    try:
        adm_command = message.text.split()
        if len(adm_command) == 3:
            command, user_id, amount = adm_command
            if command == '/add_primogems':
                await add_primogems(int(user_id), int(amount))
                await message.answer(f"Добавлено {amount} примогемов пользователю {user_id}")
            elif command == '/reduce_primogems':
                await reduce_primogems(int(user_id), int(amount))
                await message.answer(f"Уменьшено {amount} примогемов у пользователя {user_id}")
            elif command == '/ban':
                await ban_user(message, int(user_id), int(amount))
                await message.answer(f"Пользователь {user_id} заблокирован")
            elif command == '/set_promo':
                await set_promo(int(user_id), amount)
                await message.answer(f"Промокод {amount} установлен для пользователя {user_id}")
        
        elif len(adm_command) == 2:
            command, user_id = adm_command
            if command == '/delete_user':
                await delete_user(int(user_id))
                await message.answer(f"Пользователь {user_id} удален")
            
            elif command == '/get_user':
                player = await get_player(int(user_id))
                if player:
                    await message.answer(f"Пользователь {user_id} найден: @{player}")
                else:
                    await message.answer(f"Пользователь {user_id} не найден")

            

            elif command == '/unban':
                await unban_user(message, int(user_id))
                await message.answer(f"Пользователь {user_id} разблокирован")
    except Exception as e:
        await message.answer(f"Ошибка при выполнении команды: {str(e)}")
