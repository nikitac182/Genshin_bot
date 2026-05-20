from aiogram.types import CallbackQuery, Message
from database import (
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
    get_stardust,
    get_starglitter,
)
from utils import roll_rarity, update_pity
from utils1.randomizer import GachaRandomizer
from keyboards.inline import back_from_gacha_kb


async def get_reward(user_id: int, rarity: int, pity_4: int, pity_5: int, banner_type: str) -> tuple:
    """Возвращает предмет, обновлённый pity и информацию о наградах"""
    randomizer = GachaRandomizer(banner_type)
    
    stardust_gained = 0
    starglitter_gained = 0
    constellation_info = None
    
    if rarity == 3:
        item = randomizer.get_3star()
        stardust_gained = 15
        await add_weapon(user_id, item["name"], item["rarity"])
        
    elif rarity == 4:
        item = randomizer.get_4star()
        if item["type"] == "character":
            old_level, new_level = await add_character_with_constellation(user_id, item["name"], item["rarity"])
            
            if old_level is not None:
                constellation_info = f"(C{old_level} → C{new_level})"
                starglitter_gained = 2
                if old_level >= 6:
                    starglitter_gained += 3
            else:
                starglitter_gained = 0
        else:
            await add_weapon(user_id, item["name"], item["rarity"])
            starglitter_gained = 2
            
    else:
        item = randomizer.get_5star()
        if item["type"] == "character":
            old_level, new_level = await add_character_with_constellation(user_id, item["name"], item["rarity"])
            
            if old_level is not None:
                constellation_info = f"(C{old_level} → C{new_level})"
                starglitter_gained = 10
                if old_level >= 6:
                    starglitter_gained += 15
            else:
                starglitter_gained = 0
        else:
            await add_weapon(user_id, item["name"], item["rarity"])
            starglitter_gained = 10

    await add_stardust_starglitter(user_id, stardust=stardust_gained, starglitter=starglitter_gained)
    
    await add_to_wish_log(user_id, item["name"], item["rarity"])
    
    new_pity_4, new_pity_5 = await update_pity(rarity, user_id, pity_4, pity_5)
    
    return item, new_pity_4, new_pity_5, stardust_gained, starglitter_gained, constellation_info


async def wish_one_time(user_id: int, target: CallbackQuery | Message):
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

    banner_names = {
        "characters": "👥 Ивент (персонажи)",
        "weapons": "⚔️ Оружейный",
        "standard": "⭐ Стандартный"
    }
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
        f"**Баннер:** {banner_names.get(user_banner, 'Неизвестно')}\n"
        f"✨ **Получено:**\n{star_line}"
    )
    
    if isinstance(target, CallbackQuery):
        await target.message.edit_text(msg, parse_mode="Markdown", reply_markup=back_from_gacha_kb)
        await target.answer()
    else:
        await target.answer(msg)


async def wish_ten_times(user_id: int, target: CallbackQuery | Message):
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
    
    banner_names = {
        "characters": "👥 Ивентовый",
        "weapons": "⚔️ Оружейный",
        "standard": "⭐ Стандартный"
    }
    
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
        f"**Баннер:** {banner_names.get(user_banner, 'Неизвестно')}\n"
        f"✨ **Получено:**\n{star_line}"
    )
    
    if isinstance(target, CallbackQuery):
        await target.message.edit_text(msg, parse_mode="Markdown", reply_markup=back_from_gacha_kb)
        await target.answer()
    else:
        await target.answer(msg)


async def get_banner_preview_for_user(user_id: int) -> str:
    user_banner = await get_user_banner(user_id)
    randomizer = GachaRandomizer(user_banner)
    return randomizer.get_banner_preview()