PAYMENT_INSTRUCTION = (
    "Переведите {amount}₽ на карту **** ****\n\n"
    "Админ получит уведомление. После оплаты нажмите «✅ Я оплатил» "
    "или напишите админу вручную."
)

LAST = -1

TOPUP_REQUEST = (
    "💎 Запрос на пополнение:\n\n"
    "Пользователь: @{username} (id: {user_id})\n"
    "Сумма: {amount}₽ ({primogems} гемов)"
)

CONTACT_ADMIN_MESSAGE = 'Для покупки примогемов свяжитесь с администраторами:\n{admin_username}'

BANNER_NAMES = {
    "characters": "👥 Ивентовый",
    "weapons": "⚔️ Оружейный",
    "standard": "⭐ Стандартный"
}

PAYMENT_REQUEST_SENT_TEXT = (
    "Ваш запрос на пополнение отправлен администратору. "
    "Пожалуйста, дождитесь подтверждения."
)

PAYMENT_CONFIRMED_TEXT = (
    "Платеж пользователя @{username} подтвержден. "
    "Баланс обновлен."
)

HELP_TEXT = """
    🛡️ Админ команды:
    /add_primogems <user_id> <amount> - Добавить примогемы
    /reduce_primogems <user_id> <amount> - Уменьшить примогемы
    /ban <user_id> <hours> - Забанить пользователя
    /unban <user_id> - Разбанить пользователя
    /delete_user <user_id> - Удалить пользователя
    /get_user <user_id> - Информация о пользователе
    /set_promo <user_id> <promo_code> - Установить промокод для пользователя
    /help - Показать это сообщение
    """

PROFILE_CAPTION = '''
👤 Ваш профиль:

💎 Примогемов: {primogems}
🎲 Всего круток: {total_wishes}
✨ Звёздная пыль: {stardust}
⭐️ Звёздный блеск: {starglitter}

💫 Список персонажей (с созвездиями):
-{characters_list}

🗡 Выбито оружий 4★|5★:
-{weapons_list}
'''


