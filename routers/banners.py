from aiogram import Router
from aiogram.types import CallbackQuery, FSInputFile
from consts import BANNER_NAMES
from filters.ban_filter import IsNotBanned
from keyboards.inline import banner_menu_kb, menu_kb, character_choice_kb, weapon_choice_kb, weapon_banner_choice_kb, back_menu_kb
from database import set_user_banner, get_user_banner, get_banner_wishes_from_log, set_user_banner_choice, set_user_fate_point, get_user_banner_choice
from utils1.randomizer import GachaRandomizer
from datetime import datetime, timedelta
from collections import defaultdict

user_photos = defaultdict(dict)

router = Router()
router.message.filter(IsNotBanned())
router.callback_query.filter(IsNotBanned())

BANNER_IMAGES = {
    "Цзы Бай": "images/zibai_banner.jpg",
    "Нёвиллет": "images/neuvi_banner.jpg",
    "Николь": "images/nicole_banner.jpg",
    "Дурин": "images/durin_banner.jpg",
    "Ху Тао": "images/hutao_banner.jpg",
    "Е Лань": "images/yelan_banner.jpg",
    "weapons_zine": "images/weapon_zine.png",
    "weapons_nidu": "images/weapon_nidu.jpg",
    "weapons_huye": "images/weapon_huye.jpg"
}


@router.callback_query(lambda c: c.data == 'change_banner')
async def change_banner_menu(call: CallbackQuery):
    current_banner = await get_user_banner(call.from_user.id)
    banner_choice = await get_user_banner_choice(call.from_user.id, current_banner)
    if current_banner == "characters":
        if banner_choice:
            banner_name = banner_choice
        else:
            banner_name = "👥 Общий ивентовый"
        wish_in_banner = "ивентовом"
    elif current_banner == "weapons":
        if banner_choice:
            banner_name = banner_choice
        else:
            banner_name = "⚔️ Общий оружейный"
        wish_in_banner = "оружейном"
    else:
        banner_name = "⭐ Стандартный"
        wish_in_banner = "стандартном"
    banner_stats = await get_banner_wishes_from_log(call.from_user.id)
    await call.message.edit_text(
        f"🔄 **Смена баннера**\n\n"
        f"Текущий баннер: **{banner_name}**\n"
        f"Количество круток в {wish_in_banner} баннере: {banner_stats[current_banner]}\n\n"
        f"Выберите тип баннера для круток:",
        reply_markup=banner_menu_kb,
        parse_mode="Markdown"
    )
    await call.answer()

@router.callback_query(lambda c: c.data == 'banner_characters')
async def characters_banner_menu(call: CallbackQuery):
    await call.message.edit_text(
        "🎭 **Выберите тип ивентового баннера**\n\n"
        "• **Общий** — все 5★ персонажи\n",
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
    if user_id in user_photos:
        try:
            photo_info = user_photos[user_id]
            await call.bot.delete_message(
                chat_id=photo_info["chat_id"],
                message_id=photo_info["message_id"]
            )
        except:
            pass
        del user_photos[user_id]
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
    if user_id in user_photos:
        try:
            old_photo = user_photos[user_id]
            await call.bot.delete_message(
                chat_id=old_photo["chat_id"],
                message_id=old_photo["message_id"]
            )
        except:
            pass
        del user_photos[user_id]
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
            photo_msg = await call.bot.send_photo(chat_id=user_id, photo=photo)
            user_photos[user_id] = {
                "message_id": photo_msg.message_id,
                "chat_id": photo_msg.chat.id,
                "timestamp": datetime.now()
            }
        except Exception:
            pass
    await call.bot.send_message(chat_id=user_id, text=text, reply_markup=back_menu_kb, parse_mode="Markdown")
    await call.answer()

@router.callback_query(lambda c: c.data == 'banner_weapons_common')
async def set_common_weapon_banner(call: CallbackQuery):
    user_id = call.from_user.id
    if user_id in user_photos:
        try:
            photo_info = user_photos[user_id]
            await call.bot.delete_message(
                chat_id=photo_info["chat_id"],
                message_id=photo_info["message_id"]
            )
        except:
            pass
        del user_photos[user_id]
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
    if user_id in user_photos:
        try:
            photo_info = user_photos[user_id]
            await call.bot.delete_message(
                chat_id=photo_info["chat_id"],
                message_id=photo_info["message_id"]
            )
        except:
            pass
        del user_photos[user_id]
    if weapon_name in ["Светоносный осколок луны", "Обряд вечного течения"]:
        image_path = BANNER_IMAGES.get("weapons_zine")
    elif weapon_name in ["Гептада ангела", "Атаме артис"]:
        image_path = BANNER_IMAGES.get("weapons_nidu")
    else:
        image_path = BANNER_IMAGES.get("weapons_huye")
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
    await call.message.delete()
    if image_path:
        try:
            photo = FSInputFile(image_path)
            photo_msg = await call.bot.send_photo(chat_id=call.from_user.id, photo=photo)
            user_photos[user_id] = {
                "message_id": photo_msg.message_id,
                "chat_id": photo_msg.chat.id,
                "timestamp": datetime.now()
            }
        except Exception:
            pass
    await call.bot.send_message(chat_id=call.from_user.id, text=text, reply_markup=back_menu_kb, parse_mode="Markdown")
    await call.answer()

@router.callback_query(lambda c: c.data == 'banner_standard')
async def set_standard_banner(call: CallbackQuery):
    user_id = call.from_user.id
    if user_id in user_photos:
        try:
            photo_info = user_photos[user_id]
            await call.bot.delete_message(
                chat_id=photo_info["chat_id"],
                message_id=photo_info["message_id"]
            )
        except:
            pass
        del user_photos[user_id]
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