import aiosqlite
import random
from aiogram.types import CallbackQuery, Message
from consts import BANNER_NAMES
from database import (
    get_pity,
    get_primogems,
    get_user_banner,
    get_guarantee_5star,
    get_guarantee_4star,
    safe_wish,
    safe_wish_ten,
    get_user_banner_choice, 
    get_user_fate_point, 
    set_user_fate_point
)
from asyncio import Lock
from filters.ban_filter import check_user_not_banned
from utils import *
from utils1.randomizer import GachaRandomizer
from keyboards.inline import back_from_gacha_kb, group_menu_kb
from datetime import datetime, timedelta
from collections import defaultdict

_randomizer_cache = {}
_cache_timestamps = {}

def get_randomizer(banner_type: str) -> GachaRandomizer:
    if len(_randomizer_cache) > 10:
        now = datetime.now()
        to_remove = [k for k, v in _cache_timestamps.items() 
                     if now - v > timedelta(hours=1)]
        for k in to_remove:
            _randomizer_cache.pop(k, None)
            _cache_timestamps.pop(k, None)
    if banner_type not in _randomizer_cache:
        _randomizer_cache[banner_type] = GachaRandomizer(banner_type)
    return _randomizer_cache[banner_type]

user_locks = defaultdict(Lock)
user_lock_last_used = {}
def get_user_lock(user_id: int) -> Lock:
    user_lock_last_used[user_id] = datetime.now()
    lock = user_locks[user_id]
    if len(user_locks) > 100:
        cleanup_old_locks()
    return lock

def cleanup_old_locks():
    if len(user_locks) <= 100:
        return
    sorted_users = sorted(
        user_lock_last_used.items(), 
        key=lambda x: x[1], 
        reverse=True
    )[:100]
    keep_users = {user_id for user_id, _ in sorted_users}
    for uid in list(user_locks.keys()):
        if uid not in keep_users:
            del user_locks[uid]
            if uid in user_lock_last_used:
                del user_lock_last_used[uid]

async def wish_one_time(user_id: int, target: CallbackQuery | Message):
    lock = get_user_lock(user_id)
    try:
        async with lock:
            if not await check_user_not_banned(user_id):
                if isinstance(target, CallbackQuery):
                    await target.answer("Вы заблокированы.", show_alert=True)
                return
            
            user_banner = await get_user_banner(user_id)
            pity_4, pity_5 = await get_pity(user_id)
            rarity = roll_rarity(pity_4, pity_5, user_banner)
            
            (item, new_pity_4, new_pity_5, stardust_gained, starglitter_gained, 
            new_constellation_level, new_guarantee_4star, new_guarantee_5star, pity_count) = await get_reward(
                user_id, rarity, pity_4, pity_5, user_banner
            )
            
            const_line = f"(C{new_constellation_level})" if new_constellation_level is not None else ""

            success = await safe_wish(
                user_id=user_id,
                item_name=item["name"],
                item_type=item["type"],
                item_rarity=item["rarity"],
                new_pity_4=new_pity_4,
                new_pity_5=new_pity_5,
                stardust_gained=stardust_gained,
                starglitter_gained=starglitter_gained,
                banner_type=user_banner,
                pity_count=pity_count,
                new_constellation_level=new_constellation_level,
                new_guarantee_4star=new_guarantee_4star,
                new_guarantee_5star=new_guarantee_5star
            )
            if not success:
                msg = "❌ Ошибка при выполнении крутки. Попробуйте позже."
                if isinstance(target, CallbackQuery):
                    await target.answer(msg, show_alert=True)
                else:
                    await target.answer(msg)
                return

            stars = "⭐" * item["rarity"]
            
            star_text = []
            if stardust_gained > 0:
                star_text.append(f"✨ +{stardust_gained} звёздной пыли")
            if starglitter_gained > 0:
                star_text.append(f"⭐ +{starglitter_gained} звёздного блеска")
            star_line = "\n".join(star_text) if star_text else "Ничего дополнительного"
            
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
    except TimeoutError:
        msg = "⚠️ Слишком много запросов! Подождите немного."
        if isinstance(target, CallbackQuery):
            await target.answer(msg, show_alert=True)
        else:
            await target.answer(msg)

async def wish_ten_times(user_id: int, target: CallbackQuery | Message):
    lock = get_user_lock(user_id)
    try:
        async with lock:
            if not await check_user_not_banned(user_id):
                if isinstance(target, CallbackQuery):
                    await target.answer("Вы заблокированы.", show_alert=True)
                return
            
            user_banner = await get_user_banner(user_id)
            pity_4, pity_5 = await get_pity(user_id)
            guarantee_5star = await get_guarantee_5star(user_id)
            guarantee_4star = await get_guarantee_4star(user_id)
            results = []
            total_stardust = 0
            total_starglitter = 0
            wish_data = []
            current_pity_4, current_pity_5 = pity_4, pity_5
            current_guarantee_5star = guarantee_5star
            current_guarantee_4star = guarantee_4star
            temp_constellation_levels = {}

            for i in range(10):
                rarity = roll_rarity(current_pity_4, current_pity_5, user_banner)
                
                (item, new_pity_4, new_pity_5, stardust_gained, starglitter_gained, 
                 new_constellation_level, new_guarantee_4star, new_guarantee_5star, pity_count) = await get_reward(
                 user_id, rarity, current_pity_4, current_pity_5, user_banner, 
                 current_guarantee_4star, current_guarantee_5star, None
                )

                if item["type"] == "character":
                    current_level = temp_constellation_levels.get(item["name"])
                    if current_level is not None:
                        (item, new_pity_4, new_pity_5, stardust_gained, starglitter_gained, 
                        new_constellation_level, new_guarantee_4star, new_guarantee_5star, pity_count) = await get_reward(
                            user_id, rarity, current_pity_4, current_pity_5, user_banner, 
                            current_guarantee_4star, current_guarantee_5star, current_level
                        )
                    temp_constellation_levels[item["name"]] = new_constellation_level

                total_stardust += stardust_gained
                total_starglitter += starglitter_gained
                
                stars = "⭐" * item["rarity"]
                const_line = f"(C{new_constellation_level})" if new_constellation_level is not None else ""
                
                if item["rarity"] == 5 or item["rarity"] == 4:
                    results.append(f"{stars} **{item['name']}**{const_line}")
                else:
                    results.append(f"{stars} {item['name']}")
            
                wish_data.append({
                        "item_name": item["name"],
                        "item_type": item["type"],
                        "item_rarity": item["rarity"],
                        "stardust": stardust_gained,
                        "starglitter": starglitter_gained,
                        "pity_count": pity_count,
                        "constellation_level": new_constellation_level,
                        "new_guarantee_4star": new_guarantee_4star,
                        "new_guarantee_5star": new_guarantee_5star
                    })
                current_pity_4, current_pity_5 = new_pity_4, new_pity_5
                if new_guarantee_4star is not None:
                    current_guarantee_4star = new_guarantee_4star
                if new_guarantee_5star is not None:
                    current_guarantee_5star = new_guarantee_5star

            success = await safe_wish_ten(
                user_id=user_id,
                wish_data=wish_data,
                final_pity_4=current_pity_4,
                final_pity_5=current_pity_5,
                total_stardust=total_stardust,
                total_starglitter=total_starglitter,
                banner_type=user_banner
            )
            if not success:
                msg = "❌ Ошибка при выполнении круток. Попробуйте позже."
                if isinstance(target, CallbackQuery):
                    await target.answer(msg, show_alert=True)
                else:
                    await target.answer(msg)
                return
            
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
    except TimeoutError:
        msg = "⚠️ Слишком много запросов! Подождите немного."
        if isinstance(target, CallbackQuery):
            await target.answer(msg, show_alert=True)
        else:
            await target.answer(msg)

async def get_reward(user_id: int, rarity: int, pity_4: int, pity_5: int, banner_type: str, 
                    guarantee_4star: bool = None, guarantee_5star: bool = None, current_constellation_level: int = None) -> tuple:
    randomizer = get_randomizer(banner_type)
    stardust_gained = 0
    starglitter_gained = 0
    new_constellation_level = None
    pity_count = pity_5 + 1
    new_guarantee_4star = None
    new_guarantee_5star = None
    
    if rarity == 3:
        item = randomizer.get_3star()
        stardust_gained = 15
        
    elif rarity == 4:
        if guarantee_4star is None:
            guarantee_4star = await get_guarantee_4star(user_id)
        banner_choice = await get_user_banner_choice(user_id, banner_type) if banner_type in ["characters", "weapons"] else None
        featured_4star = None
        if banner_type == "characters" and banner_choice:
            banner_data = randomizer.get_character_banner_items(banner_choice)
            if banner_data:
                featured_4star = banner_data["banner_4star"]
            if featured_4star:
                item = randomizer.get_4star_with_featured(guarantee_4star, featured_4star)
            else:
                item = randomizer.get_4star(guarantee_4star)
        elif banner_type == "weapons" and banner_choice:
            randomizer_temp = GachaRandomizer(banner_type)
            banner_data = randomizer_temp.get_weapon_banner_items(banner_choice)
            featured_4star = banner_data.get("featured_4star") if banner_data else None
            if featured_4star:
                item = randomizer.get_4star_with_featured_weapons(guarantee_4star, featured_4star)
            else:
                item = randomizer.get_4star(guarantee_4star)
        else:
            item = randomizer.get_4star(guarantee_4star)
        if item["type"] == "character":
            old_level = current_constellation_level
            if old_level is None:
                async with aiosqlite.connect('sqlite.db') as db:
                    async with db.execute(
                        'SELECT constellation_level FROM inventory WHERE user_id = ? AND item_name = ? AND item_type = "character"',
                        (user_id, item["name"])
                    ) as cursor:
                        result = await cursor.fetchone()
                        old_level = result[0] if result else -1
            if old_level == -1:
                new_constellation_level = 0
                starglitter_gained = 0
            else:
                new_constellation_level = old_level + 1
                starglitter_gained = 2
                if old_level >= 6:
                    starglitter_gained += 3
            if banner_type != "weapons":
                new_guarantee_4star = False
            else:
                new_guarantee_4star = True 
        else:
            starglitter_gained = 2
            new_constellation_level = None
            if banner_type != "weapons":
                new_guarantee_4star = True
            else:
                new_guarantee_4star = False
    else:
        if guarantee_5star is None:
            guarantee_5star = await get_guarantee_5star(user_id)
        banner_choice = await get_user_banner_choice(user_id, banner_type) if banner_type in ["characters", "weapons"] else None
        
        if banner_type == "characters" and banner_choice:
            if guarantee_5star:
                item = {"name": banner_choice, "type": "character", "rarity": 5}
                new_guarantee_5star = False
            else:
                if random.random() < 0.5:
                    item = {"name": banner_choice, "type": "character", "rarity": 5}
                    new_guarantee_5star = False
                else:
                    item = {"name": random.choice(randomizer.standard_5star_characters), "type": "character", "rarity": 5}
                    new_guarantee_5star = True
            old_level = current_constellation_level
            if old_level is None:
                async with aiosqlite.connect('sqlite.db') as db:
                    async with db.execute(
                        'SELECT constellation_level FROM inventory WHERE user_id = ? AND item_name = ? AND item_type = "character"',
                        (user_id, item["name"])
                    ) as cursor:
                        result = await cursor.fetchone()
                        old_level = result[0] if result else -1
            if old_level == -1:
                new_constellation_level = 0
                starglitter_gained = 0
            else:
                new_constellation_level = old_level + 1
                starglitter_gained = 10
                if old_level >= 6:
                    starglitter_gained += 15  
        elif banner_type == "weapons" and banner_choice:
            fate_point = await get_user_fate_point(user_id)
            result = randomizer.get_5star_with_path(guarantee_5star, banner_choice, fate_point)
            item = {"name": result["name"], "type": "weapon", "rarity": 5}
            if result.get("fate_point_used"):
                await set_user_fate_point(user_id, 0)
                new_guarantee_5star = False
            elif result.get("fate_point_gained"):
                await set_user_fate_point(user_id, 1)
                new_guarantee_5star = True
            else:
                await set_user_fate_point(user_id, 0)
                new_guarantee_5star = False
            if result.get("guarantee_used"):
                new_guarantee_5star = False
            starglitter_gained = 10
            new_constellation_level = None
            
        else:
            item = randomizer.get_5star(guarantee_5star)
            new_guarantee_4star = None
            
            if item["type"] == "character":
                old_level = current_constellation_level
                if old_level is None:
                    async with aiosqlite.connect('sqlite.db') as db:
                        async with db.execute(
                            'SELECT constellation_level FROM inventory WHERE user_id = ? AND item_name = ? AND item_type = "character"',
                            (user_id, item["name"])
                        ) as cursor:
                            result = await cursor.fetchone()
                            old_level = result[0] if result else -1
                if old_level == -1:
                    new_constellation_level = 0
                    starglitter_gained = 0
                else:
                    new_constellation_level = old_level + 1
                    starglitter_gained = 10
                    if old_level >= 6:
                        starglitter_gained += 15
            else:
                starglitter_gained = 10
                new_constellation_level = None
            
            if banner_type == "characters":
                if item["name"] in randomizer.standard_5star_characters:
                    new_guarantee_5star = True
                else:
                    new_guarantee_5star = False
            else:
                new_guarantee_5star = None
        
        new_guarantee_4star = None
    new_pity_4, new_pity_5 = await update_pity(rarity, pity_4, pity_5)
    
    return (item, new_pity_4, new_pity_5, stardust_gained, starglitter_gained, 
            new_constellation_level, new_guarantee_4star, new_guarantee_5star, pity_count)

async def get_banner_preview_for_user(user_id: int) -> str:
    user_banner = await get_user_banner(user_id)
    randomizer = GachaRandomizer(user_banner)
    return randomizer.get_banner_preview()