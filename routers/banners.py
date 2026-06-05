from aiogram import Router
from aiogram.types import CallbackQuery, FSInputFile
from consts import BANNER_NAMES
from filters.ban_filter import IsNotBanned
from keyboards.inline import banner_menu_kb, menu_kb, character_choice_kb, weapon_choice_kb, weapon_banner_choice_kb
from database import set_user_banner, get_user_banner, get_banner_wishes_from_log, set_user_banner_choice, set_user_fate_point
from utils1.randomizer import GachaRandomizer

router = Router()
router.message.filter(IsNotBanned())
router.callback_query.filter(IsNotBanned())

BANNER_IMAGES = {
    "Цзы Бай": "images/zibai_banner.jpg",
    "Нёвиллет": "images/neuvi_banner.jpg",
    "weapons": "images/weapon_banner.png"
}


@router.callback_query(lambda c: c.data == 'change_banner')
async def change_banner_menu(call: CallbackQuery):
    current_banner = await get_user_banner(call.from_user.id)
    banner_name = BANNER_NAMES.get(current_banner, "Неизвестно")
    banner_stats = await get_banner_wishes_from_log(call.from_user.id)

    await call.message.edit_text(
        f"🔄 **Смена баннера**\n\n"
        f"Текущий баннер: **{banner_name}**\n"
        f"Количество круток на этом баннере: {banner_stats[current_banner]}\n\n"
        f"Выберите тип баннера для круток:",
        reply_markup=banner_menu_kb,
        parse_mode="Markdown"
    )
    await call.answer()

@router.callback_query(lambda c: c.data == 'banner_characters')
async def characters_banner_menu(call: CallbackQuery):
    await call.message.edit_text(
        "🎭 **Выберите тип ивентового баннера**\n\n"
        "• **Общий** — все 5★ персонажи\n"
        "• **Цзы Бай**\n"
        "• **Нёвиллет**\n\n"
        "🎭 Ивентовые 4★: Иллуги, Айно, Горо",
        reply_markup=character_choice_kb,
        parse_mode="Markdown"
    )
    await call.answer()

@router.callback_query(lambda c: c.data == 'banner_weapons')
async def weapons_banner_menu(call: CallbackQuery):
    await call.message.edit_text(
        "⚔️ **Выберите тип оружейного баннера**\n\n"
        "• **Общий** — все 5★ оружие\n"
        "• **Цзы Бай/Нёвиллет**",
        reply_markup=weapon_banner_choice_kb,
        parse_mode="Markdown"
    )
    await call.answer()

@router.callback_query(lambda c: c.data == 'banner_weapons_path')
async def weapons_path_menu(call: CallbackQuery):
    await call.message.edit_text(
        "⚔️ **Выберите оружие для пути**\n\n"
        "Выберите оружие, которое хотите выбить:\n\n"
        "💫 **Механика оружейного баннера с путём:**\n"
        "• 75% шанс выпадения ивентового оружия\n"
        "• При проигрыше вы получаете очко судьбы\n"
        "• С очком судьбы следующее 5★ оружие — гарантированно выбранное!",
        reply_markup=weapon_choice_kb,
        parse_mode="Markdown"
    )
    await call.answer()

@router.callback_query(lambda c: c.data == 'banner_characters_common')
async def set_common_character_banner(call: CallbackQuery):
    user_id = call.from_user.id
    await set_user_banner_choice(user_id, "characters", None)
    await set_user_banner(user_id, "characters")
    await set_user_fate_point(user_id, 0)
    
    await call.message.edit_text(
        f"✅ Баннер сменён на **Общий ивентовый**!\n\n"
        f"📊 Здесь вы можете получить любого 5★ персонажа.\n",
        reply_markup=menu_kb,
        parse_mode="Markdown"
    )
    await call.answer()

@router.callback_query(lambda c: c.data.startswith('banner_characters_') and c.data not in ['banner_characters', 'banner_characters_common'])
async def set_specific_character_banner(call: CallbackQuery):
    character_name = call.data.split('_')[2]
    user_id = call.from_user.id
    randomizer = GachaRandomizer("characters")
    banner_data = randomizer.get_character_banner_items(character_name)
    if banner_data:
        featured_4star = ", ".join(banner_data["banner_4star"])
        four_star_text = f"\n🎭 Повышенные 4★: {featured_4star}"
    else:
        four_star_text = ""
    await set_user_banner_choice(user_id, "characters", character_name)
    await set_user_banner(user_id, "characters")
    await set_user_fate_point(user_id, 0)
    image_path = BANNER_IMAGES.get(character_name)
    text = f"✅ Баннер сменён на **{character_name}**!\n\n" \
           f"🎭 50/50 шанс выпадения {character_name}\n" \
           f"{four_star_text}"
    await call.message.delete()
    if image_path:
        try:
            photo = FSInputFile(image_path)
            await call.message.answer_photo(photo=photo)
        except Exception:
            pass
    await call.message.answer(text, reply_markup=menu_kb, parse_mode="Markdown")
    await call.answer()

@router.callback_query(lambda c: c.data == 'banner_weapons_common')
async def set_common_weapon_banner(call: CallbackQuery):
    user_id = call.from_user.id
    await set_user_banner_choice(user_id, "weapons", None)
    await set_user_banner(user_id, "weapons")
    await set_user_fate_point(user_id, 0)
    await call.message.edit_text(
        f"✅ Баннер сменён на **Общий оружейный**!\n\n"
        f"📊 Здесь вы можете получить любое 5★ оружие.\n",
        reply_markup=menu_kb,
        parse_mode="Markdown"
    )
    await call.answer()

@router.callback_query(lambda c: c.data.startswith('banner_weapon_'))
async def set_path_weapon_banner(call: CallbackQuery):
    weapon_name = call.data.split('_')[-1]
    user_id = call.from_user.id
    if weapon_name == "Lightbearing_Moonshard" or weapon_name == "Moonshard":
        weapon_name = "Светоносный осколок луны"
    elif weapon_name == "TotEF":
        weapon_name = "Обряд вечного течения"
    randomizer_temp = GachaRandomizer("weapons")
    banner_data = randomizer_temp.get_weapon_banner_items(weapon_name)
    featured_4star = banner_data.get("featured_4star", []) if banner_data else []
    four_star_text = f"\n⚔️ Повышенные 4★ оружия: {', '.join(featured_4star)}" if featured_4star else ""
    await set_user_banner_choice(user_id, "weapons", weapon_name)
    await set_user_banner(user_id, "weapons")
    await set_user_fate_point(user_id, 0)
    text = (f"✅ Путь сменён на **{weapon_name}**!\n\n" \
           f"📊 Теперь вы будете крутить с выбором пути.\n" \
           f"⚡ При проигрыше вы получите очко судьбы!"
           f"{four_star_text}")
    image_path = BANNER_IMAGES.get("weapons")
    await call.message.delete()
    if image_path:
        try:
            photo = FSInputFile(image_path)
            await call.message.answer_photo(photo=photo)
        except Exception:
            pass
    await call.message.answer(text, reply_markup=menu_kb, parse_mode="Markdown")
    await call.answer()

@router.callback_query(lambda c: c.data == 'banner_standard')
async def set_standard_banner(call: CallbackQuery):
    user_id = call.from_user.id
    await set_user_banner(user_id, "standard")
    await set_user_fate_point(user_id, 0)
    
    await call.message.edit_text(
        f"✅ Баннер сменён на **Стандартный**!\n\n"
        f"📊 50% шанс выпадения персонажа, 50% — оружия.",
        reply_markup=menu_kb,
        parse_mode="Markdown"
    )
    await call.answer()

@router.callback_query(lambda c: c.data == 'back_to_menu')
async def back_to_menu(call: CallbackQuery):
    await call.message.edit_text("🏠 **Главное меню**", reply_markup=menu_kb, parse_mode="Markdown")
    await call.answer()