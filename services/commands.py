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
            elif command == '/set_promo':
                code = user_id
                reward = amount
                await set_promo(code, int(reward))
                await message.answer(f"✅ Промокод `{code}` | {reward}💎 | 1 раз")

        elif len(adm_command) == 4:
            command, code, reward, max_uses = adm_command
            if command == '/set_promo':
                await set_promo(code, int(reward), int(max_uses))
                await message.answer(f"✅ `{code}` | {reward}💎 | {max_uses} раз")
        
        elif len(adm_command) == 5:
            command, code, reward, max_uses, expires = adm_command
            if command == '/set_promo':
                await set_promo(code, int(reward), int(max_uses), int(expires))
                await message.answer(f"✅ `{code}` | {reward}💎 | {max_uses} раз | {expires}ч")

        elif len(adm_command) == 1:
            command = adm_command[0]
            if command == '/list_promo':
                promos = await get_all_promocodes()
                if not promos:
                    await message.answer("📋 Список промокодов пуст.")
                else:
                    from datetime import datetime
                    
                    text = "📋 **Промокоды:**\n\n"
                    for promo in promos:
                        code, reward, max_uses, used_count, expires_at, used_by, created_at = promo
                        
                        if expires_at:
                            expires_date = datetime.fromisoformat(expires_at)
                            if datetime.now() > expires_date:
                                status = "❌ истёк"
                            else:
                                status = "✅ активен"
                        else:
                            if used_count >= max_uses:
                                status = "❌ кончился"
                            else:
                                status = "✅ активен"
                        
                        text += f"`{code}` | {reward}💎 | {used_count}/{max_uses} | {status}\n"
                    await message.answer(text, parse_mode="Markdown")

        elif len(adm_command) == 2:
            command, user_id = adm_command
            if command == '/delete_user':
                await delete_user(int(user_id))
                await message.answer(f"Пользователь {user_id} удален")
            
            elif command == '/del_promo':
                await del_promo(user_id)
                await message.answer(f"✅ Промокод `{user_id}` удалён!")

            elif command == '/unban':
                await unban_user(message, int(user_id))
    except Exception as e:
        await message.answer(f"Ошибка при выполнении команды: {str(e)}")
