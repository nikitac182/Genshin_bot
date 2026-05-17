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