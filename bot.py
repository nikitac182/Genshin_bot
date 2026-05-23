import asyncio
import aiosqlite
from aiogram import Bot, Dispatcher
from config import TOKEN
from routers.admin import router as admin_router
from routers.start import router as start_router
from routers.wishes import router as wishes_router
from routers.profile import router as profile_router
from routers.shop import router as shop_router
from routers.leaderboard import router as leaderboard_router
from routers.banners import router as banner_router
from routers.exchange import router as exchange_router
from routers.group_start import router as group_router
from services.hourly_reward import start_hourly_reward
from routers.subscription import router as subscription_router
from database import get_status
    
bot = Bot(TOKEN)
dp = Dispatcher()


async def main():

    db = await aiosqlite.connect('sqlite.db')
    dp.include_router(group_router)
    dp.include_router(start_router)
    dp.include_router(wishes_router)
    dp.include_router(profile_router)
    dp.include_router(shop_router)
    dp.include_router(leaderboard_router)
    dp.include_router(banner_router)
    dp.include_router(exchange_router)
    dp.include_router(subscription_router)
    dp.include_router(admin_router)

    await db.executescript(
        '''
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
        stardust INTEGER DEFAULT 0,
        starglitter INTEGER DEFAULT 0,
        hour_reward DATETIME DEFAULT CURRENT_TIMESTAMP,
        current_banner TEXT DEFAULT 'characters',
        is_subscribed INTEGER DEFAULT 0,
        is_banned INTEGER DEFAULT 0,
        ban_end_time DATETIME
        );

        CREATE TABLE IF NOT EXISTS inventory 
        (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        item_name TEXT,
        item_type TEXT,
        rarity INTEGER,
        constellation_level INTEGER DEFAULT 0,
        refinement_level INTEGER DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS wish_log 
        (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        item_name TEXT,
        rarity INTEGER,
        current_banner TEXT DEFAULT 'characters',
        pity_count INTEGER DEFAULT 0,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP    
        );

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
        );
        '''
    )

    await db.commit()

    await start_hourly_reward()
    
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())