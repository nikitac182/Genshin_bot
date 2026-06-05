from aiogram.types import *
from config import CHANNEL_LINK


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
            InlineKeyboardButton(text="🔄 Сменить баннер", callback_data="change_banner"),
            InlineKeyboardButton(text="📢 Бонус за подписку", callback_data="subscription_info")
        ],
    ]
)

def group_menu_kb(user_id: int):
    return InlineKeyboardMarkup(
    inline_keyboard = [
            [
                InlineKeyboardButton(text="🔮 Крутить 1", callback_data=f"wish_1_{user_id}"),
                InlineKeyboardButton(text="🔟 Крутить 10", callback_data=f"wish_10_{user_id}")
            ],
            [
                InlineKeyboardButton(text="👤 Профиль", callback_data=f"profile_{user_id}")
            ],
        ]
    )

back_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_menu"),
        ],
    ]
)

confirm_payment_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Подтвердить", callback_data="admin_confirm_payment"),
            InlineKeyboardButton(text="❌ Отмена", callback_data="admin_cancel_payment")
        ],
    ]
)

profile_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="💫 Персонажи", callback_data="show_characters"),
            InlineKeyboardButton(text="🗡 Оружие", callback_data="show_weapons")
        ],
        [InlineKeyboardButton(text="🎫 Ввести промокод", callback_data="promo_code")],
        [InlineKeyboardButton(text="🕒 История круток", callback_data="story_wishes")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_menu")],
    ]
)

def profile_menu_kb(user_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_menu")],
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
            InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_menu"),
        ],
    ]
)

def admin_confirm_kb(user_id: int, primogems: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Подтвердить", callback_data=f"admin_confirm_{user_id}_{primogems}"),
                InlineKeyboardButton(text="❌ Отмена", callback_data=f"admin_cancel_{user_id}")
            ]
        ]
    )

payment_confirm_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Я оплатил", callback_data="confirm_payment"),
            InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_payment")
        ]
    ]
)

banner_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="👥 Ивентовый", callback_data="banner_characters"),
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

subscription_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📢 Подписаться на канал", url=CHANNEL_LINK)],
        [InlineKeyboardButton(text="🔗 Проверить подписку", callback_data="check_subscription")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_menu")],
    ]
)

promo_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🎫 Ввести промокод", callback_data="promo_code")],
        [InlineKeyboardButton(text="🔙 Назад в профиль", callback_data="profile")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_menu")]
    ]
)

close_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="❌ Закрыть", callback_data="close_list")]
    ]
)

leaderboard_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🔍 Топ по персонажу", callback_data="leaderboard_character"),
            InlineKeyboardButton(text="⚔️ Топ по оружию", callback_data="leaderboard_weapon")
        ],
        [
            InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_menu")
        ],
    ]
)

lb_back_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🎲 Топ по круткам", callback_data="leaderboard")
        ],
        [
            InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_menu")
        ],
    ]
)

character_choice_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="👥 Общий", callback_data="banner_characters_common"),
            InlineKeyboardButton(text="Цзы Бай", callback_data="banner_characters_Цзы Бай"),
            InlineKeyboardButton(text="Нёвиллет", callback_data="banner_characters_Нёвиллет")
        ],
        [
            InlineKeyboardButton(text="🔙 Назад", callback_data="change_banner")
        ],
    ]
)

weapon_banner_choice_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="⚔️ Общий", callback_data="banner_weapons_common"),
            InlineKeyboardButton(text="Цзы Бай/Нёвиллет", callback_data="banner_weapons_path"),
        ],
        [
            InlineKeyboardButton(text="🔙 Назад", callback_data="change_banner")
        ],
    ]
)

weapon_choice_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Светоносный осколок луны", callback_data="banner_weapon_Lightbearing_Moonshard"),
            InlineKeyboardButton(text="Обряд вечного течения", callback_data="banner_weapon_TotEF")
        ],
        [
            InlineKeyboardButton(text="🔙 Назад", callback_data="change_banner")
        ],
    ]
)