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
        [
            InlineKeyboardButton(text="🔄 Сменить баннер", callback_data="change_banner")
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

wish_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️", callback_data="prev_wishes"),
            InlineKeyboardButton(text="➡️", callback_data="next_wishes")
        ],
        [
            InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_menu")
        ],
    ]
)

profile_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🕒 История круток", callback_data="story_wishes")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_menu_from_profile")],
    ]
)

shop_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="💎 1600 гемов – 10 руб", callback_data="buy_1600_10"), 
            InlineKeyboardButton(text="💎 3200 гемов – 20 руб", callback_data="buy_3200_20")
        ],
        [
            InlineKeyboardButton(text="💎 12000 гемов – 50 руб", callback_data="buy_12000_50"), 
            InlineKeyboardButton(text="💎 32000 гемов – 100 руб", callback_data="buy_32000_100")
        ],
        [
            InlineKeyboardButton(text="💎 96000 гемов – 300 руб", callback_data="buy_96000_300"), 
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

banner_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="👥 Ивент (персонажи)", callback_data="banner_characters"),
            InlineKeyboardButton(text="⚔️ Оружейный", callback_data="banner_weapons")
        ],
        [
            InlineKeyboardButton(text="⭐ Стандартный", callback_data="banner_standard"),
        ],
        [
            InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_menu")
        ],
    ]
)

back_from_gacha_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🔮 Крутить 1", callback_data="wish_1"),
            InlineKeyboardButton(text="🔟 Крутить 10", callback_data="wish_10")
        ],
        [
            InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_menu")
        ],

    ]
)