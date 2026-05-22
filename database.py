#database.py
import aiosqlite

from config import COUNT_WISHES_PER_PAGE

async def add_user(user_id, username, name):
    async with aiosqlite.connect('sqlite.db') as db:
        await db.execute('INSERT OR IGNORE INTO users (user_id, username, name) VALUES (?, ?, ?)', (user_id, username, name))
        await db.commit()

async def add_item(user_id, item_name, item_type, rarity):
    async with aiosqlite.connect('sqlite.db') as db:
        await db.execute('INSERT INTO inventory (user_id, item_name, item_type, rarity) VALUES (?, ?, ?, ?)', (user_id, item_name, item_type, rarity))
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
        
async def get_rarity(user_id):
    async with aiosqlite.connect('sqlite.db') as db:
        async with db.execute('SELECT rarity FROM users WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else None
        
async def get_pity(user_id):
    async with aiosqlite.connect('sqlite.db') as db:
        async with db.execute('SELECT pity_4, pity_5 FROM users WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchone()
            return (result[0], result[1]) if result else (None, None)

async def reduce_primogems(user_id, amount):
    '''Уменьшает количество примогемов у пользователя на указанную сумму.'''
    async with aiosqlite.connect('sqlite.db') as db:
        await db.execute('UPDATE users SET primogems = primogems - ? WHERE user_id = ?', (amount, user_id))
        await db.commit()

async def pull_pity(user_id, new_pity_4, new_pity_5):
    async with aiosqlite.connect('sqlite.db') as db:
        await db.execute('UPDATE users SET pity_4 = ?, pity_5 = ? WHERE user_id = ?', (new_pity_4, new_pity_5, user_id))
        await db.commit()

async def pull_rarity(user_id, rarity):
    async with aiosqlite.connect('sqlite.db') as db:
        await db.execute('UPDATE inventory SET rarity = rarity - ? WHERE user_id = ?', (rarity, user_id))
        await db.commit()

async def pull_total_wishes(user_id, amount):
    '''Увеличивает общее количество круток пользователя на указанную сумму.'''
    async with aiosqlite.connect('sqlite.db') as db:
        await db.execute('UPDATE users SET total_wishes = total_wishes + ? WHERE user_id = ?', (amount, user_id))
        await db.commit()

async def get_character_constellation(user_id: int, character_name: str) -> int:
    async with aiosqlite.connect('sqlite.db') as db:
        async with db.execute(
            'SELECT constellation_level FROM inventory WHERE user_id = ? AND item_name = ? AND item_type = "character"',
            (user_id, character_name)
        ) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else 0

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

async def update_character_constellation(user_id: int, character_name: str, new_level: int):
    async with aiosqlite.connect('sqlite.db') as db:
        await db.execute(
            'UPDATE inventory SET constellation_level = ? WHERE user_id = ? AND item_name = ? AND item_type = "character"',
            (new_level, user_id, character_name)
        )
        await db.commit()

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


async def add_to_wish_log(user_id: int, item_name: str, rarity: int):
    """Добавляет запись в лог круток"""
    async with aiosqlite.connect('sqlite.db') as db:
        await db.execute(
            'INSERT INTO wish_log (user_id, item_name, rarity) VALUES (?, ?, ?)',
            (user_id, item_name, rarity)
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
            'SELECT item_name, rarity, current_banner, timestamp FROM wish_log WHERE user_id = ? ORDER BY timestamp DESC LIMIT ? OFFSET ?',
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