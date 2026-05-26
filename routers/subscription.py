from aiogram import Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import set_user_subscription, get_user_subscription
from filters.ban_filter import IsNotBanned
from config import CHANNEL_ID, CHANNEL_LINK

router = Router()
router.message.filter(IsNotBanned())
router.callback_query.filter(IsNotBanned())


main_menu_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_menu")]
    ]
)

@router.callback_query(lambda c: c.data == 'check_subscription')
async def check_subscription(call: types.CallbackQuery):
    user_id = call.from_user.id
    
    try:
        member = await call.bot.get_chat_member(CHANNEL_ID, user_id)
        is_subscribed = member.status in ['member', 'creator', 'administrator']
    except:
        is_subscribed = False
    
    if is_subscribed:
        await set_user_subscription(user_id, True)
        await call.message.edit_text(
            "✅ **Подписка подтверждена!**\n\n"
            "Теперь вы будете получать **150 примогемов** в час вместо обычных 100.\n\n",
            reply_markup=main_menu_button,
            parse_mode="Markdown"
        )
    else:
        await set_user_subscription(user_id, False)
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📢 Подписаться на канал", url=CHANNEL_LINK)],
            [InlineKeyboardButton(text="🔄 Проверить подписку", callback_data="check_subscription")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_menu")]
        ])
        await call.message.delete()
        await call.message.answer(
            "❌ **Вы не подписаны на канал!**\n\n"
            "Подпишитесь на наш канал, чтобы получать **150 примогемов** в час вместо 100.\n\n"
            "После подписки нажмите «Проверить подписку».",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
    await call.answer()


@router.callback_query(lambda c: c.data == 'subscription_info')
async def subscription_info(call: types.CallbackQuery):
    user_id = call.from_user.id
    try:
        member = await call.bot.get_chat_member(CHANNEL_ID, user_id)
        is_subscribed = member.status in ['member', 'creator', 'administrator']
    except:
        is_subscribed = False
    await set_user_subscription(user_id, is_subscribed)

    current_reward = 150 if is_subscribed else 100
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔗 Проверить подписку", callback_data="check_subscription")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_menu")]
    ])
    
    status_text = "✅ **Подписка активна!**" if is_subscribed else "❌ **Подписка не активна**"
    
    await call.message.edit_text(
        f"📢 **Бонус за подписку**\n\n"
        f"{status_text}\n\n"
        f"💰 Текущая награда: **{current_reward} примогемов** в час\n"
        f"⭐ Максимальная награда: **150 примогемов** в час\n\n"
        f"Подпишитесь на канал, чтобы увеличить награду!",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    await call.answer()