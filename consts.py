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


