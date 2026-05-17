from aiogram.types import *

menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🔮 Крутить 1", callback_data="wish_1"),
            InlineKeyboardButton(text="🔟 Крутить 10", callback_data="wish_10")
        ],
        [
            InlineKeyboardButton(text="👤 Профиль", callback_data="profile"),
            InlineKeyboardButton(text="💎 Купить примогемы", callback_data="primogems_buy")
        ],
        [
            InlineKeyboardButton(text="🏆 Лидерборд", callback_data="leaderboard"),
            InlineKeyboardButton(text="✨ Обмен пыли и блеска", callback_data="exchange")
        ],
    ]
)

back_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_menu_from_profile"),
        ],
    ]
)

shop_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="💎 1600 гемов – 10 руб", callback_data="buy_1600_10"), 
            InlineKeyboardButton(text="💎 3200 гемов – 20 руб", callback_data="buy_3200_20")
        ],
        [
            InlineKeyboardButton(text="💎 8000 гемов – 50 руб", callback_data="buy_8000_50"), 
            InlineKeyboardButton(text="💎 16000 гемов – 100 руб", callback_data="buy_16000_100")
        ],
        [
            InlineKeyboardButton(text="💎 48000 гемов – 300 руб", callback_data="buy_48000_300"), 
        ],
        [
            InlineKeyboardButton(text="📞 Связаться с админом для начисления", callback_data="contact_admin"), 
        ],
        [
            InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_menu_from_profile"),
        ],
    ]
)

payment_confirm_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="✅ Я оплатил", callback_data="confirm_payment"),
        InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_payment")
    ]
])