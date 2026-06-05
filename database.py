#database.py
import aiosqlite
from datetime import datetime, timedelta
from config import COUNT_WISHES_PER_PAGE
from utils1.randomizer import get_all_5star_characters, get_all_4star_characters, get_all_5star_weapons, get_all_4star_weapons

async def add_user(user_id, username, name):
    async with aiosqlite.connect('sqlite.db') as db:
        await db.execute('INSERT OR IGNORE INTO users (user_id, username, name, start_count) VALUES (?, ?, ?, 0)', (user_id, username, name))
        await db.commit()

async def add_primogems(user_id, amount):
    async with aiosqlite.connect('sqlite.db') as db:
        await db.execute('UPDATE users SET primogems = primogems + ? WHERE user_id = ?', (amount, user_id))
        await db.commit()

async def delete_user(user_id):
    async with aiosqlite.connect('sqlite.db') as db:
        await db.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
        await db.execute('DELETE FROM inventory WHERE user_id = ?', (user_id,))
        await db.execute('DELETE FROM wish_log WHERE user_id = ?', (user_id,))
        async with db.execute('SELECT code, used_by FROM promocodes') as cursor:
            promos = await cursor.fetchall()
            for code, used_by in promos:
                if used_by:
                    used_list = used_by.split(',')
                    if str(user_id) in used_list:
                        used_list.remove(str(user_id))
                        new_used_by = ','.join(used_list) if used_list else ''
                        await db.execute(
                            'UPDATE promocodes SET used_by = ? WHERE code = ?',
                            (new_used_by, code)
                        )
        await db.commit()

async def get_status(user_id):
    async with aiosqlite.connect('sqlite.db') as db:
        async with db.execute('SELECT is_banned FROM users WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchone()
            if result:
                is_banned = result[0]
                if is_banned:
                    return 'banned'
            return 'active'

async def update_user_ban_status(user_id, is_banned: bool, ban_end_time=None):
    async with aiosqlite.connect('sqlite.db') as db:
        await db.execute('UPDATE users SET is_banned = ?, ban_end_time = ? WHERE user_id = ?', (1 if is_banned else 0, ban_end_time, user_id))
        await db.commit()

async def get_player(user_id):
    async with aiosqlite.connect('sqlite.db') as db:
        async with db.execute('SELECT user_id, username FROM users WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchone()
            return result[1] if result else None

async def get_primogems(user_id):
    async with aiosqlite.connect('sqlite.db') as db:
        async with db.execute('SELECT primogems FROM users WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else None
        
async def get_total_wishes(user_id):
    async with aiosqlite.connect('sqlite.db') as db:
        async with db.execute('SELECT total_wishes FROM users WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else None
        
async def get_users_for_leaderboard():
    async with aiosqlite.connect('sqlite.db') as db:
        async with db.execute('SELECT name, username, user_id, total_wishes FROM users ORDER BY total_wishes DESC LIMIT 10') as cursor:
            result = await cursor.fetchall()
            return result
        
async def get_stardust(user_id):
    async with aiosqlite.connect('sqlite.db') as db:
        async with db.execute('SELECT stardust FROM users WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else 0
        
async def get_starglitter(user_id):
    async with aiosqlite.connect('sqlite.db') as db:
        async with db.execute('SELECT starglitter FROM users WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else 0

async def get_pity(user_id):
    async with aiosqlite.connect('sqlite.db') as db:
        async with db.execute('SELECT pity_4, pity_5 FROM users WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchone()
            return (result[0], result[1]) if result else (0, 0)

async def get_guarantee_5star(user_id: int) -> bool:
    async with aiosqlite.connect('sqlite.db') as db:
        async with db.execute('SELECT guarantee_5star FROM users WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchone()
            return result[0] == 1 if result else False

async def set_guarantee_5star(user_id: int, guaranteed: bool):
    async with aiosqlite.connect('sqlite.db') as db:
        await db.execute('UPDATE users SET guarantee_5star = ? WHERE user_id = ?', (1 if guaranteed else 0, user_id))
        await db.commit()

async def get_guarantee_4star(user_id: int) -> bool:
    async with aiosqlite.connect('sqlite.db') as db:
        async with db.execute('SELECT guarantee_4star FROM users WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchone()
            return result[0] == 1 if result else False

async def set_guarantee_4star(user_id: int, guaranteed: bool):
    async with aiosqlite.connect('sqlite.db') as db:
        await db.execute('UPDATE users SET guarantee_4star = ? WHERE user_id = ?', (1 if guaranteed else 0, user_id))
        await db.commit()

async def reduce_primogems(user_id, amount):
    '''Уменьшает количество примогемов у пользователя на указанную сумму.'''
    async with aiosqlite.connect('sqlite.db') as db:
        await db.execute('UPDATE users SET primogems = primogems - ? WHERE user_id = ?', (amount, user_id))
        await db.commit()

async def pull_pity(user_id, new_pity_4, new_pity_5):
    async with aiosqlite.connect('sqlite.db') as db:
        await db.execute('UPDATE users SET pity_4 = ?, pity_5 = ? WHERE user_id = ?', (new_pity_4, new_pity_5, user_id))
        await db.commit()

async def pull_total_wishes(user_id, amount):
    '''Увеличивает общее количество круток пользователя на указанную сумму.'''
    async with aiosqlite.connect('sqlite.db') as db:
        await db.execute('UPDATE users SET total_wishes = total_wishes + ? WHERE user_id = ?', (amount, user_id))
        await db.commit()

async def get_wish_result_data(user_id: int) -> dict:
    async with aiosqlite.connect('sqlite.db') as db:
        cursor = await db.execute(
            '''SELECT primogems, current_banner, stardust 
               FROM users WHERE user_id = ?''',
            (user_id,)
        )
        row = await cursor.fetchall()
        
        return row[0] if row else None

async def get_characters_with_constellation(user_id: int) -> list:
    async with aiosqlite.connect('sqlite.db') as db:
        async with db.execute(
            'SELECT item_name, constellation_level, rarity FROM inventory WHERE user_id = ? AND item_type = "character" ORDER BY rarity DESC, item_name',
            (user_id,)
        ) as cursor:
            result = await cursor.fetchall()
            return [(row[0], row[1], row[2]) for row in result] if result else []

async def add_character_with_constellation(user_id: int, character_name: str, rarity: int):
    async with aiosqlite.connect('sqlite.db') as db:
        async with db.execute(
            'SELECT id, constellation_level FROM inventory WHERE user_id = ? AND item_name = ? AND item_type = "character"',
            (user_id, character_name)
        ) as cursor:
            existing = await cursor.fetchone()
        
        if existing:
            current_level = existing[1]
            new_level = current_level + 1
            
            await db.execute(
                'UPDATE inventory SET constellation_level = ? WHERE id = ?',
                (new_level, existing[0])
            )
            await db.commit()
            return current_level, new_level
        else:
            await db.execute(
                'INSERT INTO inventory (user_id, item_name, item_type, rarity, constellation_level) VALUES (?, ?, ?, ?, ?)',
                (user_id, character_name, "character", rarity, 0)
            )
            await db.commit()
            return None, 0

async def add_weapon(user_id: int, weapon_name: str, rarity: int):
    async with aiosqlite.connect('sqlite.db') as db:
        await db.execute(
            'INSERT INTO inventory (user_id, item_name, item_type, rarity, constellation_level) VALUES (?, ?, ?, ?, ?)',
            (user_id, weapon_name, "weapon", rarity, 0)
        )
        await db.commit()

async def add_weapon_with_refinement(user_id: int, weapon_name: str, rarity: int):
    async with aiosqlite.connect('sqlite.db') as db:
        async with db.execute(
            'SELECT id, refinement_level FROM inventory WHERE user_id = ? AND item_name = ? AND item_type = "weapon"',
            (user_id, weapon_name)
        ) as cursor:
            existing = await cursor.fetchone()
        
        if existing:
            current_level = existing[1]
            new_level = current_level + 1
            
            await db.execute(
                'UPDATE inventory SET refinement_level = ? WHERE id = ?',
                (new_level, existing[0])
            )
            await db.commit()
            return current_level, new_level
        else:
            await db.execute(
                'INSERT INTO inventory (user_id, item_name, item_type, rarity, refinement_level) VALUES (?, ?, ?, ?, ?)',
                (user_id, weapon_name, "weapon", rarity, 1)  # начинаем с R1
            )
            await db.commit()
            return None, 1

async def get_weapons_with_refinement(user_id: int) -> list:
    async with aiosqlite.connect('sqlite.db') as db:
        async with db.execute(
            'SELECT item_name, refinement_level, rarity FROM inventory WHERE user_id = ? AND item_type = "weapon" AND rarity >= 4 ORDER BY rarity DESC, item_name',
            (user_id,)
        ) as cursor:
            result = await cursor.fetchall()
            return [(row[0], row[1], row[2]) for row in result] if result else []

async def get_user_banner(user_id: int) -> str:
    async with aiosqlite.connect('sqlite.db') as db:
        async with db.execute('SELECT current_banner FROM users WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchone()
            return result[0] if result and result[0] else "characters"

async def set_user_banner(user_id: int, banner_type: str):
    async with aiosqlite.connect('sqlite.db') as db:
        await db.execute('UPDATE users SET current_banner = ? WHERE user_id = ?', (banner_type, user_id))
        await db.commit()

async def set_current_banner(item_id: int, banner_type: str):
    async with aiosqlite.connect('sqlite.db') as db:
        await db.execute('UPDATE wish_log SET current_banner = ? WHERE id = ?', (banner_type, item_id))
        await db.commit()

async def add_stardust_starglitter(user_id: int, stardust: int = 0, starglitter: int = 0):
    """Добавляет звёздную пыль и блеск пользователю"""
    async with aiosqlite.connect('sqlite.db') as db:
        if stardust > 0:
            await db.execute('UPDATE users SET stardust = stardust + ? WHERE user_id = ?', (stardust, user_id))
        if starglitter > 0:
            await db.execute('UPDATE users SET starglitter = starglitter + ? WHERE user_id = ?', (starglitter, user_id))
        await db.commit()

async def add_to_wish_log(user_id: int, item_name: str, rarity: int, pity_count: int = 0, banner_type: str = None):
    """Добавляет запись в лог круток"""
    async with aiosqlite.connect('sqlite.db') as db:
        await db.execute(
            'INSERT INTO wish_log (user_id, item_name, rarity, pity_count, current_banner) VALUES (?, ?, ?, ?, ?)',
            (user_id, item_name, rarity, pity_count, banner_type)
        )
        await db.commit()

async def get_id_by_wish_log_entry(user_id: int, item_name: str, rarity: int) -> int:
    """Получает ID записи в wish_log по данным крутки"""
    async with aiosqlite.connect('sqlite.db') as db:
        async with db.execute(
            'SELECT id FROM wish_log WHERE user_id = ? AND item_name = ? AND rarity = ? ORDER BY timestamp DESC LIMIT 1',
            (user_id, item_name, rarity)
        ) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else None

async def data_wishes(user_id: int, offset: int = 0) -> list:
    """Получает историю круток пользователя"""
    async with aiosqlite.connect('sqlite.db') as db:
        async with db.execute(
            'SELECT item_name, rarity, current_banner, pity_count, timestamp FROM wish_log WHERE user_id = ? ORDER BY timestamp DESC, id DESC LIMIT ? OFFSET ?',
            (user_id, COUNT_WISHES_PER_PAGE, offset)
        ) as cursor:
            result = await cursor.fetchall()
            return result if result else []

async def get_user_subscription(user_id: int) -> bool:
    async with aiosqlite.connect('sqlite.db') as db:
        async with db.execute('SELECT is_subscribed FROM users WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchone()
            return result[0] == 1 if result else False

async def set_user_subscription(user_id: int, subscribed: bool):
    async with aiosqlite.connect('sqlite.db') as db:
        await db.execute('UPDATE users SET is_subscribed = ? WHERE user_id = ?', (1 if subscribed else 0, user_id))
        await db.commit()

async def set_promo(code: str, reward: int, max_uses: int = 1, expires_hours: int = None):
    expires_at = None
    if expires_hours:
        expires_at = (datetime.now() + timedelta(hours=expires_hours)).isoformat()
    
    async with aiosqlite.connect('sqlite.db') as db:
        await db.execute(
            'INSERT INTO promocodes (code, reward, max_uses, expires_at) VALUES (?, ?, ?, ?)',
            (code, reward, max_uses, expires_at)
        )
        await db.commit()

async def get_promocode_info(code: str) -> tuple:
    async with aiosqlite.connect('sqlite.db') as db:
        async with db.execute(
            'SELECT code, reward, max_uses, used_count, expires_at, used_by FROM promocodes WHERE code = ?',
            (code,)
        ) as cursor:
            result = await cursor.fetchone()
            return result if result else None

async def use_promocode(code: str, user_id: int) -> tuple:
    from datetime import datetime
    
    async with aiosqlite.connect('sqlite.db') as db:
        async with db.execute(
            'SELECT reward, max_uses, used_count, expires_at, used_by FROM promocodes WHERE code = ?',
            (code,)
        ) as cursor:
            promo = await cursor.fetchone()
        
        if not promo:
            return False, "❌ Промокод не найден!", 0
        
        reward, max_uses, used_count, expires_at, used_by = promo
        
        if expires_at:
            expires_date = datetime.fromisoformat(expires_at)
            if datetime.now() > expires_date:
                return False, "❌ Срок действия промокода истёк!", 0
        
        if used_count >= max_uses:
            return False, "❌ Лимит активация промокода", 0
        
        used_list = used_by.split(',') if used_by else []
        if str(user_id) in used_list:
            return False, "❌ Вы уже использовали этот промокод!", 0
        
        new_used_count = used_count + 1
        new_used_by = ','.join(used_list + [str(user_id)]) if used_list else str(user_id)
        
        await db.execute(
            'UPDATE promocodes SET used_count = ?, used_by = ? WHERE code = ?',
            (new_used_count, new_used_by, code)
        )
        await db.commit()
        
        return True, f"✅ Промокод активирован! Вы получили {reward} гемов.", reward

async def get_all_promocodes() -> list:
    async with aiosqlite.connect('sqlite.db') as db:
        async with db.execute(
            'SELECT code, reward, max_uses, used_count, expires_at, used_by, created_at FROM promocodes ORDER BY created_at DESC'
        ) as cursor:
            result = await cursor.fetchall()
            return result if result else []

async def del_promo(code: str):
    async with aiosqlite.connect('sqlite.db') as db:
        await db.execute('DELETE FROM promocodes WHERE code = ?', (code,))
        await db.commit()

async def is_first_start(user_id: int) -> bool:
    async with aiosqlite.connect('sqlite.db') as db:
        async with db.execute(
            'SELECT start_count FROM users WHERE user_id = ?',
            (user_id,)
        ) as cursor:
            result = await cursor.fetchone()
            # Если записи нет или start_count = 0, то первый запуск
            return not result or result[0] == 0

async def increment_start_count(user_id: int):
    async with aiosqlite.connect('sqlite.db') as db:
        await db.execute(
            'UPDATE users SET start_count = start_count + 1 WHERE user_id = ?',
            (user_id,)
        )
        await db.commit()

async def get_banner_wishes_from_log(user_id: int) -> dict:
    async with aiosqlite.connect('sqlite.db') as db:
        async with db.execute(
            'SELECT current_banner, COUNT(*) FROM wish_log WHERE user_id = ? GROUP BY current_banner',
            (user_id,)
        ) as cursor:
            rows = await cursor.fetchall() 
        stats = {
            'characters': 0,
            'weapons': 0,
            'standard': 0,
            'total': 0
        }
        for banner, count in rows:
            if banner in stats:
                stats[banner] = count
            stats['total'] += count
        return stats

async def execute_wish_transaction(user_id: int, operations: list) -> bool:
    async with aiosqlite.connect('sqlite.db') as db:
        try:
            await db.execute('BEGIN TRANSACTION')
            
            for sql, params in operations:
                await db.execute(sql, params)
            
            await db.commit()
            return True
        except Exception as e:
            await db.rollback()
            print(f"Транзакция откачена: {e}")
            return False

async def safe_wish(user_id: int, item_name: str, item_type: str, item_rarity: int,
                          new_pity_4: int, new_pity_5: int, stardust_gained: int, 
                          starglitter_gained: int, banner_type: str, pity_count: int,
                          new_constellation_level: int = None,
                          new_guarantee_4star: bool = None, new_guarantee_5star: bool = None) -> bool:
    async with aiosqlite.connect('sqlite.db') as db:
        try:
            await db.execute('BEGIN TRANSACTION')
            cursor = await db.execute('UPDATE users SET primogems = primogems - 160 WHERE user_id = ? AND primogems >= 160', (user_id,))
            if cursor.rowcount == 0:
                await db.rollback()
                return False
            await db.execute('UPDATE users SET total_wishes = total_wishes + 1 WHERE user_id = ?', (user_id,))
            await db.execute('UPDATE users SET pity_4 = ?, pity_5 = ? WHERE user_id = ?', (new_pity_4, new_pity_5, user_id))
            if new_guarantee_4star is not None:
                await db.execute('UPDATE users SET guarantee_4star = ? WHERE user_id = ?', (1 if new_guarantee_4star else 0, user_id))
            if new_guarantee_5star is not None:
                await db.execute('UPDATE users SET guarantee_5star = ? WHERE user_id = ?', (1 if new_guarantee_5star else 0, user_id))
            if stardust_gained > 0 or starglitter_gained > 0:
                await db.execute('UPDATE users SET stardust = stardust + ?, starglitter = starglitter + ? WHERE user_id = ?',
                               (stardust_gained, starglitter_gained, user_id))
            await db.execute(
                'INSERT INTO wish_log (user_id, item_name, rarity, pity_count, current_banner) VALUES (?, ?, ?, ?, ?)',
                (user_id, item_name, item_rarity, pity_count, banner_type)
            )
            if item_type == "character":
                async with db.execute(
                    'SELECT id, constellation_level FROM inventory WHERE user_id = ? AND item_name = ? AND item_type = "character"',
                    (user_id, item_name)
                ) as cursor:
                    existing = await cursor.fetchone()
                if existing:
                    await db.execute('UPDATE inventory SET constellation_level = constellation_level + 1 WHERE id = ?', (existing[0],))
                else:
                    level = new_constellation_level if new_constellation_level is not None else 0
                    await db.execute(
                        'INSERT INTO inventory (user_id, item_name, item_type, rarity, constellation_level) VALUES (?, ?, ?, ?, ?)',
                        (user_id, item_name, "character", item_rarity, level)
                    )
            else:
                async with db.execute(
                    'SELECT id, refinement_level FROM inventory WHERE user_id = ? AND item_name = ? AND item_type = "weapon"',
                    (user_id, item_name)
                ) as cursor:
                    existing = await cursor.fetchone()
                if existing:
                    await db.execute('UPDATE inventory SET refinement_level = refinement_level + 1 WHERE id = ?', 
                                   (existing[0],))
                else:
                    await db.execute(
                        'INSERT INTO inventory (user_id, item_name, item_type, rarity, refinement_level) VALUES (?, ?, ?, ?, ?)',
                        (user_id, item_name, "weapon", item_rarity, 1)
                    )
            await db.commit()
            return True
        except Exception as e:
            await db.rollback()
            print(f"❌ Транзакция отказана для {user_id}: {e}")
            return False

async def safe_wish_ten(user_id: int, wish_data: list, final_pity_4: int, final_pity_5: int,
                         total_stardust: int, total_starglitter: int, banner_type: str) -> bool:
    async with aiosqlite.connect('sqlite.db') as db:
        try:
            await db.execute('BEGIN TRANSACTION')
            cursor = await db.execute('UPDATE users SET primogems = primogems - 1600 WHERE user_id = ? AND primogems >= 1600', (user_id,))
            if cursor.rowcount == 0:
                await db.rollback()
                return False
            await db.execute('UPDATE users SET total_wishes = total_wishes + 10 WHERE user_id = ?', (user_id,))
            await db.execute('UPDATE users SET pity_4 = ?, pity_5 = ? WHERE user_id = ?', (final_pity_4, final_pity_5, user_id))
            if total_stardust > 0 or total_starglitter > 0:
                await db.execute('UPDATE users SET stardust = stardust + ?, starglitter = starglitter + ? WHERE user_id = ?',
                               (total_stardust, total_starglitter, user_id))
            for data in wish_data:
                await db.execute(
                    'INSERT INTO wish_log (user_id, item_name, rarity, pity_count, current_banner) VALUES (?, ?, ?, ?, ?)',
                    (user_id, data["item_name"], data["item_rarity"], data["pity_count"], banner_type)
                )
                if data["item_type"] == "character":
                    async with db.execute(
                        'SELECT id, constellation_level FROM inventory WHERE user_id = ? AND item_name = ? AND item_type = "character"',
                        (user_id, data["item_name"])
                    ) as cursor:
                        existing = await cursor.fetchone()
                    if existing:
                        await db.execute('UPDATE inventory SET constellation_level = constellation_level + 1 WHERE id = ?', (existing[0],))
                    else:
                        level = data["constellation_level"] if data["constellation_level"] is not None else 0
                        await db.execute(
                            'INSERT INTO inventory (user_id, item_name, item_type, rarity, constellation_level) VALUES (?, ?, ?, ?, ?)',
                            (user_id, data["item_name"], "character", data["item_rarity"], level)
                        )
                else:
                    async with db.execute(
                        'SELECT id, refinement_level FROM inventory WHERE user_id = ? AND item_name = ? AND item_type = "weapon"',
                        (user_id, data["item_name"])
                    ) as cursor:
                        existing = await cursor.fetchone()
                    if existing:
                        await db.execute('UPDATE inventory SET refinement_level = refinement_level + 1 WHERE id = ?', (existing[0],))
                    else:
                        await db.execute(
                            'INSERT INTO inventory (user_id, item_name, item_type, rarity, refinement_level) VALUES (?, ?, ?, ?, ?)',
                            (user_id, data["item_name"], "weapon", data["item_rarity"], 1)
                        )
                if data["new_guarantee_4star"] is not None:
                    await db.execute('UPDATE users SET guarantee_4star = ? WHERE user_id = ?', 
                                   (1 if data["new_guarantee_4star"] else 0, user_id))
                if data["new_guarantee_5star"] is not None:
                    await db.execute('UPDATE users SET guarantee_5star = ? WHERE user_id = ?', 
                                   (1 if data["new_guarantee_5star"] else 0, user_id))
            await db.commit()
            return True
            
        except Exception as e:
            await db.rollback()
            print(f"❌ Транзакция 10 круток отказана для {user_id}: {e}")
            return False

async def get_users_for_character_leaderboard(character_name: str) -> list:    
    async with aiosqlite.connect('sqlite.db') as db:
        async with db.execute("""SELECT u.name, u.username, u.user_id, i.constellation_level FROM inventory i JOIN users u 
            ON u.user_id = i.user_id WHERE i.item_name = ? AND i.item_type = 'character' ORDER BY i.constellation_level DESC, u.total_wishes DESC LIMIT 10""", 
            (character_name,)
        ) as cursor:
            result = await cursor.fetchall()
            return result if result else []

async def get_user_rank_by_character(user_id: int, character_name: str) -> int:
    async with aiosqlite.connect('sqlite.db') as db:
        async with db.execute("""SELECT COUNT(*) + 1 FROM inventory i WHERE i.item_name = ? AND i.item_type = 'character'
            AND i.constellation_level > (SELECT COALESCE(constellation_level, -1) FROM inventory WHERE user_id = ? AND item_name = ? AND item_type = 'character')""", 
            (character_name, user_id, character_name)
        ) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else 1

async def get_total_character_owners(character_name: str) -> int:
    async with aiosqlite.connect('sqlite.db') as db:
        async with db.execute(
            """SELECT COUNT(*) FROM inventory WHERE item_name = ? AND item_type = 'character'""", 
            (character_name,)
        ) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else 0

async def get_users_for_weapon_leaderboard(weapon_name: str) -> list:    
    async with aiosqlite.connect('sqlite.db') as db:
        async with db.execute("""
            SELECT u.name, u.username, u.user_id, i.refinement_level FROM inventory i JOIN users u ON u.user_id = i.user_id 
            WHERE i.item_name = ? AND i.item_type = 'weapon' AND i.rarity = 5 ORDER BY i.refinement_level DESC, u.total_wishes DESC LIMIT 10""", 
            (weapon_name,)
        ) as cursor:
            result = await cursor.fetchall()
            return result if result else []

async def get_user_weapon_rank(user_id: int, weapon_name: str) -> int:
    async with aiosqlite.connect('sqlite.db') as db:
        async with db.execute("""
            SELECT COUNT(*) + 1 FROM inventory i WHERE i.item_name = ? AND i.item_type = 'weapon' AND i.rarity = 5
            AND i.refinement_level > (SELECT COALESCE(refinement_level, 0) FROM inventory WHERE user_id = ? AND item_name = ? AND item_type = 'weapon')""", 
            (weapon_name, user_id, weapon_name)
        ) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else 1

async def get_total_weapon_owners(weapon_name: str) -> int:
    async with aiosqlite.connect('sqlite.db') as db:
        async with db.execute(
            """SELECT COUNT(*) FROM inventory WHERE item_name = ? AND item_type = 'weapon' AND rarity = 5""", 
            (weapon_name,)
        ) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else 0

async def find_character_by_name(name: str) -> str | None:
    all_characters = get_all_5star_characters() + get_all_4star_characters()
    for char in all_characters:
        if char.lower() == name.lower():
            return char
    async with aiosqlite.connect('sqlite.db') as db:
        async with db.execute(
            """SELECT DISTINCT item_name FROM inventory WHERE item_type = 'character' AND LOWER(item_name) = LOWER(?) LIMIT 1""",
            (name,)
        ) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else None

async def find_weapon_by_name(name: str) -> str | None:
    all_weapons = get_all_5star_weapons() + get_all_4star_weapons()
    for weapon in all_weapons:
        if weapon.lower() == name.lower():
            return weapon
    async with aiosqlite.connect('sqlite.db') as db:
        async with db.execute(
            """SELECT DISTINCT item_name FROM inventory WHERE item_type = 'weapon' AND rarity = 5 AND LOWER(item_name) = LOWER(?) LIMIT 1""",
            (name,)
        ) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else None
        
async def get_user_banner_choice(user_id: int, banner_type: str) -> str:
    async with aiosqlite.connect('sqlite.db') as db:
        async with db.execute(
            'SELECT banner_choice FROM user_banner_choices WHERE user_id = ? AND banner_type = ?',
            (user_id, banner_type)
        ) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else None
        
async def set_user_banner_choice(user_id: int, banner_type: str, choice: str):
    async with aiosqlite.connect('sqlite.db') as db:
        await db.execute(
            'INSERT OR REPLACE INTO user_banner_choices (user_id, banner_type, banner_choice) VALUES (?, ?, ?)',
            (user_id, banner_type, choice)
        )
        await db.commit()

async def get_user_fate_point(user_id: int) -> int:
    async with aiosqlite.connect('sqlite.db') as db:
        async with db.execute(
            'SELECT fate_point FROM users WHERE user_id = ?',
            (user_id,)
        ) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else 0

async def set_user_fate_point(user_id: int, fate_point: int):
    async with aiosqlite.connect('sqlite.db') as db:
        await db.execute(
            'UPDATE users SET fate_point = ? WHERE user_id = ?',
            (fate_point, user_id)
        )
        await db.commit()