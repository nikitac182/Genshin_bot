from aiogram.types import CallbackQuery, Message
from aiogram import F
from aiogram.fsm.context import FSMContext
from consts import BANNER_NAMES, CONTACT_ADMIN_MESSAGE, PROFILE_CAPTION
from keyboards.inline import *
from database import *
from services.paginator import get_wish_menu_kb, get_page, get_max_page
from state.promocode_state import PromoState


async def set_story_wishes(call: CallbackQuery, offset: int = 0):
    wishes = await data_wishes(call.from_user.id, offset=offset)
    page = await get_page(call.from_user.id, offset=offset)
    max_page = await get_max_page(call.from_user.id, offset=offset)
    caption = '📜 История круток:\n'
    if not wishes:
        caption = "📜 История круток пуста."
    else:
        for wish in wishes:
            item_name, rarity, current_banner, timestamp = wish
            caption += f'''
═══════════════
{'⭐'*rarity} {item_name}
Баннер: {BANNER_NAMES.get(current_banner, 'Неизвестно')}
Время: {timestamp}'''
        
    await call.message.edit_text(
        caption + f"\n\nСтраница {page + 1} из {max_page + 1}" if max_page != -1 else caption,
        reply_markup=await get_wish_menu_kb(
            page,
            max_page
        ),
        parse_mode='HTML'
    )

async def set_profile(call: CallbackQuery, user_in_profile_id):
    if user_in_profile_id != call.from_user.id:
        await call.answer()
        return
    primogems = await get_primogems(call.from_user.id)
    total_wishes = await get_total_wishes(call.from_user.id)
    stardust = await get_stardust(call.from_user.id)
    starglitter = await get_starglitter(call.from_user.id)
    characters = await get_characters_with_constellation(call.from_user.id)
    weapons = await get_weapons_with_refinement(call.from_user.id)
    caption = PROFILE_CAPTION.format(
        primogems=primogems,
        total_wishes=total_wishes,
        stardust=stardust,
        starglitter=starglitter,
        characters_list="\n-".join(f"{name} (C{level})" for name, level, _ in characters),
        weapons_list="\n-".join(f"{name} (R{level})" for name, level, _ in weapons)
    )
    await call.message.edit_text(caption, reply_markup=profile_kb if call.message.chat.type == "private" else profile_menu_kb(call.from_user.id))

async def set_promo_code(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        "🎫 Введите промокод для получения награды:",
        reply_markup=back_menu_kb
    )
    await state.set_state(PromoState.waiting_for_promo_code)

async def process_promo_code(message: Message, state: FSMContext):
    user_text = message.text.strip()
    user_id = message.from_user.id
    promo_info = await get_promocode_info(user_text)

    if not promo_info:
        await message.answer(
            "❌ Неверный промокод. Пожалуйста, попробуйте снова или обратитесь к администратору.",
            reply_markup=back_menu_kb
        )
        await state.clear()
        return
    
    code, reward, max_uses, used_count, expires_at, used_by = promo_info

    if expires_at:
        from datetime import datetime
        expires_date = datetime.fromisoformat(expires_at)
        if datetime.now() > expires_date:
            await message.answer(
                "❌ Срок действия промокода истёк!",
                reply_markup=back_menu_kb,
            )
            await state.clear()
            return
    
    if used_count >= max_uses:
        await message.answer(
            f"❌ Лимит активация промокода",
            reply_markup=back_menu_kb,
        )
        await state.clear()
        return

    used_list = used_by.split(',') if used_by else []
    if str(user_id) in used_list:
        await message.answer(
            "❌ Вы уже использовали этот промокод!",
            reply_markup=back_menu_kb,
        )
        await state.clear()
        return
    
    success, msg, reward_amount = await use_promocode(code, user_id)
    if success:
        await add_primogems(user_id, reward_amount)
        remaining = max_uses - (used_count + 1)

        await message.answer(
            f"✅ Промокод успешно активирован! Вы получили награду в размере {reward_amount} примогемов!",
            reply_markup=back_menu_kb
        )
    else:
        await message.answer(
            f"{msg}",
            reply_markup=back_menu_kb,
        )

    await state.clear()