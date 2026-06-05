import aiosqlite
from datetime import datetime, timedelta


async def run_migrations():
    async with aiosqlite.connect('sqlite.db') as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users 
            (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            username TEXT UNIQUE,
            name TEXT,
            primogems INTEGER DEFAULT 8000,
            total_wishes INTEGER DEFAULT 0,
            pity_4 INTEGER DEFAULT 0,
            pity_5 INTEGER DEFAULT 0,
            guarantee_5star INTEGER DEFAULT 0,
            guarantee_4star INTEGER DEFAULT 0,
            stardust INTEGER DEFAULT 0,
            starglitter INTEGER DEFAULT 0,
            hour_reward DATETIME DEFAULT CURRENT_TIMESTAMP,
            current_banner TEXT DEFAULT 'characters',
            is_subscribed INTEGER DEFAULT 0,
            is_banned INTEGER DEFAULT 0,
            ban_end_time DATETIME,
            start_count INTEGER DEFAULT 0
            )
        ''')
        
        await add_column_if_not_exists(db, 'users', 'fate_point', 'INTEGER DEFAULT 0')
        
        await db.execute('''
            CREATE TABLE IF NOT EXISTS inventory 
            (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            item_name TEXT,
            item_type TEXT,
            rarity INTEGER,
            constellation_level INTEGER DEFAULT 0,
            refinement_level INTEGER DEFAULT 1
            )
        ''')
        
        await db.execute('''
            CREATE TABLE IF NOT EXISTS wish_log 
            (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            item_name TEXT,
            rarity INTEGER,
            current_banner TEXT DEFAULT 'characters',
            pity_count INTEGER DEFAULT 0,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP    
            )
        ''')
        
        await db.execute('''
            CREATE TABLE IF NOT EXISTS promocodes 
            (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE,
            reward INTEGER,
            max_uses INTEGER DEFAULT 1,
            used_count INTEGER DEFAULT 0,
            expires_at DATETIME,
            used_by TEXT DEFAULT '',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        await db.execute('''
            CREATE TABLE IF NOT EXISTS user_banner_choices 
            (
            user_id INTEGER,
            banner_type TEXT,
            banner_choice TEXT,
            PRIMARY KEY (user_id, banner_type)
            )
        ''')
        
        await db.commit()


async def add_column_if_not_exists(db, table, column, column_type):
    try:
        async with db.execute(f"PRAGMA table_info({table})") as cursor:
            columns = await cursor.fetchall()
            column_names = [col[1] for col in columns]
        
        if column not in column_names:
            await db.execute(f"ALTER TABLE {table} ADD COLUMN {column} {column_type}")
            print(f"✅ Добавлена колонка {column} в таблицу {table}")
    except Exception as e:
        print(f"⚠️ Ошибка при добавлении колонки {column}: {e}")