#database.py
import aiosqlite

async def add_user(user_id, username):
    async with aiosqlite.connect('sqlite.db') as db:
        await db.execute('INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)', (user_id, username))
        await db.commit()

async def add_item(user_id, item_name, item_type, rarity):
    async with aiosqlite.connect('sqlite.db') as db:
        await db.execute('INSERT INTO inventory (user_id, item_name, item_type, rarity) VALUES (?, ?, ?, ?)', (user_id, item_name, item_type, rarity))
        await db.commit()

async def add_primogems(user_id, amount):
    async with aiosqlite.connect('sqlite.db') as db:
        await db.execute('UPDATE users SET primogems = primogems + ? WHERE user_id = ?', (amount, user_id))
        await db.commit()

async def get_player(user_id):
    async with aiosqlite.connect('sqlite.db') as db:
        async with db.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else None

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
        async with db.execute('SELECT username, total_wishes FROM users ORDER BY total_wishes DESC LIMIT 10') as cursor:
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
            new_level = min(current_level + 1, 6)
            
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

async def get_user_banner(user_id: int) -> str:
    async with aiosqlite.connect('sqlite.db') as db:
        async with db.execute('SELECT current_banner FROM users WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchone()
            return result[0] if result and result[0] else "characters"

async def set_user_banner(user_id: int, banner_type: str):
    async with aiosqlite.connect('sqlite.db') as db:
        await db.execute('UPDATE users SET current_banner = ? WHERE user_id = ?', (banner_type, user_id))
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