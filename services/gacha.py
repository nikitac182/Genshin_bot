from aiogram.types import CallbackQuery, Message
from consts import BANNER_NAMES
from database import (
    get_id_by_wish_log_entry,
    get_pity,
    get_primogems,
    pull_pity,
    pull_total_wishes,
    reduce_primogems,
    add_to_wish_log,
    add_stardust_starglitter,
    get_user_banner,
    add_character_with_constellation,
    add_weapon,
    set_current_banner,
    get_guarantee_5star,
    set_guarantee_5star,
    get_guarantee_4star,
    set_guarantee_4star,
)
from filters.ban_filter import check_user_not_banned
from utils import roll_rarity, update_pity
from utils1.randomizer import GachaRandomizer
from keyboards.inline import back_from_gacha_kb, group_menu_kb
from database import add_weapon_with_refinement

async def wish_one_time(user_id: int, target: CallbackQuery | Message):

    if not await check_user_not_banned(user_id):
        if isinstance(target, CallbackQuery):
            await target.answer("Вы заблокированы.", show_alert=True)
        return
    
    primogems = await get_primogems(user_id)
    
    if primogems < 160:
        msg = "❌ Недостаточно примогемов!"
        if isinstance(target, CallbackQuery):
            await target.answer(msg, show_alert=True)
        else:
            await target.answer(msg)
        return
    
    user_banner = await get_user_banner(user_id)
    await reduce_primogems(user_id, 160)
    await pull_total_wishes(user_id, 1)
    
    pity_4, pity_5 = await get_pity(user_id)
    
    rarity = roll_rarity(pity_4, pity_5, user_banner)
    
    item, new_pity_4, new_pity_5, stardust_gained, starglitter_gained, constellation_info = await get_reward(
        user_id, rarity, pity_4, pity_5, user_banner
    )
    
    await pull_pity(user_id, new_pity_4, new_pity_5)

    stars = "⭐" * item["rarity"]
    
    star_text = []
    if stardust_gained > 0:
        star_text.append(f"✨ +{stardust_gained} звёздной пыли")
    if starglitter_gained > 0:
        star_text.append(f"⭐ +{starglitter_gained} звёздного блеска")
    star_line = "\n".join(star_text) if star_text else "Ничего дополнительного"

    const_line = f"{constellation_info}" if constellation_info else ""
    
    msg = (
        f"Вы получили:\n"
        f"{stars} **{item['name']}**{const_line}\n\n"
        f"💎 Осталось примогемов: {await get_primogems(user_id)}\n"
        f"**Баннер:** {BANNER_NAMES.get(user_banner, 'Неизвестно')}\n"
        f"✨ **Получено:**\n{star_line}"
    )
    
    if isinstance(target, CallbackQuery):
        await target.message.edit_text(
            msg,
            parse_mode="Markdown",
            reply_markup=back_from_gacha_kb if target.message.chat.type == 'private' else group_menu_kb(target.from_user.id))
        await target.answer()
    else:
        await target.answer(msg)

async def wish_ten_times(user_id: int, target: CallbackQuery | Message):

    if not await check_user_not_banned(user_id):
        if isinstance(target, CallbackQuery):
            await target.answer("Вы заблокированы.", show_alert=True)
        return
    
    primogems = await get_primogems(user_id)
    
    if primogems < 1600:
        msg = "❌ Недостаточно примогемов!"
        if isinstance(target, CallbackQuery):
            await target.answer(msg, show_alert=True)
        else:
            await target.answer(msg)
        return
    
    user_banner = await get_user_banner(user_id)
    await reduce_primogems(user_id, 1600)
    await pull_total_wishes(user_id, 10)
    
    pity_4, pity_5 = await get_pity(user_id)
    
    results = []
    total_stardust = 0
    total_starglitter = 0

    for i in range(10):
        rarity = roll_rarity(pity_4, pity_5, user_banner)
        
        item, new_pity_4, new_pity_5, stardust_gained, starglitter_gained, constellation_info = await get_reward(
            user_id, rarity, pity_4, pity_5, user_banner
        )

        total_stardust += stardust_gained
        total_starglitter += starglitter_gained
        
        pity_4, pity_5 = new_pity_4, new_pity_5
        
        stars = "⭐" * item["rarity"]

        const_line = f"{constellation_info}" if constellation_info else ""
        
        if item["rarity"] == 5 or item["rarity"] == 4:
            results.append(f"{stars} **{item['name']}**{const_line}")
        else:
            results.append(f"{stars} {item['name']}")
    
    await pull_pity(user_id, pity_4, pity_5)
    
    star_text = []
    if total_stardust > 0:
        star_text.append(f"✨ +{total_stardust} звёздной пыли")
    if total_starglitter > 0:
        star_text.append(f"⭐ +{total_starglitter} звёздного блеска")
    star_line = "\n".join(star_text) if star_text else "Ничего дополнительного"

    results_text = "\n".join(results)
    msg = (
        f"Вы получили:\n"
        f"{results_text}\n\n"
        f"💎 Осталось примогемов: {await get_primogems(user_id)}\n"
        f"**Баннер:** {BANNER_NAMES.get(user_banner, 'Неизвестно')}\n"
        f"✨ **Получено:**\n{star_line}"
    )
    
    if isinstance(target, CallbackQuery):
        await target.message.edit_text(msg, parse_mode="Markdown", reply_markup=back_from_gacha_kb if target.message.chat.type == 'private' else group_menu_kb(target.from_user.id))
        await target.answer()
    else:
        await target.answer(msg)

async def get_reward(user_id: int, rarity: int, pity_4: int, pity_5: int, banner_type: str) -> tuple:
    """Возвращает предмет, обновлённый pity и информацию о наградах"""
    randomizer = GachaRandomizer(banner_type)
    
    stardust_gained = 0
    starglitter_gained = 0
    constellation_info = None

    pity_count = pity_5 + 1
    
    if rarity == 3:
        item = randomizer.get_3star()
        stardust_gained = 15
        await add_weapon(user_id, item["name"], item["rarity"])
        
    elif rarity == 4:
        guarantee_4star = await get_guarantee_4star(user_id)
        item = randomizer.get_4star(guarantee_4star)
        if item["type"] == "character":
            old_level, new_level = await add_character_with_constellation(user_id, item["name"], item["rarity"])
            if banner_type != "weapons":
                await set_guarantee_4star(user_id, False)
            else:
                await set_guarantee_4star(user_id, True)
            
            if old_level is not None:
                constellation_info = f"(C{new_level})"
                starglitter_gained = 2
                if old_level >= 6:
                    starglitter_gained += 3
            else:
                starglitter_gained = 0
                constellation_info = "(C0)"
        else: 
            if banner_type != "weapons":
                await set_guarantee_4star(user_id, True)
            else:
                await set_guarantee_4star(user_id, False)
            old_level, new_level = await add_weapon_with_refinement(user_id, item["name"], item["rarity"])
            starglitter_gained = 2
                
            
    else:
        guarantee_5star = await get_guarantee_5star(user_id)
        item = randomizer.get_5star(guarantee_5star)
        if item["type"] == "character":
            old_level, new_level = await add_character_with_constellation(user_id, item["name"], item["rarity"])
            if banner_type == "characters":
                if item["name"] in randomizer.standard_5star_characters:
                    await set_guarantee_5star(user_id, True)
                else:
                    await set_guarantee_5star(user_id, False)
                
            if old_level is not None:
                constellation_info = f"(C{new_level})"
                starglitter_gained = 10
                if old_level >= 6:
                    starglitter_gained += 15
            else:
                starglitter_gained = 0
                constellation_info = "(C0)"
        else:
            if banner_type == "weapons":
                if item["name"] in randomizer.standart_weapons_5star:
                    await set_guarantee_5star(user_id, True)
                else:
                    await set_guarantee_5star(user_id, False)
            old_level, new_level = await add_weapon_with_refinement(user_id, item["name"], item["rarity"])
            starglitter_gained = 10

    await add_stardust_starglitter(user_id, stardust=stardust_gained, starglitter=starglitter_gained)
    await add_to_wish_log(user_id, item["name"], item["rarity"], pity_count)
    item_id = await get_id_by_wish_log_entry(user_id, item["name"], item["rarity"])
    await set_current_banner(item_id, banner_type)
    new_pity_4, new_pity_5 = await update_pity(rarity, user_id, pity_4, pity_5)
    
    return item, new_pity_4, new_pity_5, stardust_gained, starglitter_gained, constellation_info


async def get_banner_preview_for_user(user_id: int) -> str:

    user_banner = await get_user_banner(user_id)
    randomizer = GachaRandomizer(user_banner)
    return randomizer.get_banner_preview()