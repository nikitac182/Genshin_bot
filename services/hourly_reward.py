import asyncio
import aiosqlite
from datetime import datetime, timedelta
from aiogram import Bot
from config import TOKEN, REWARD_NON_SUBSCRIBED, REWARD_SUBSCRIBED, CHANNEL_ID
from collections import defaultdict

bot = Bot(token=TOKEN)
_subscription_cache = {}
CACHE_TTL = timedelta(minutes=30)

async def check_subscription_status(user_id: int, force: bool = False) -> bool:
    now = datetime.now()
    if not force and user_id in _subscription_cache:
        status, timestamp = _subscription_cache[user_id]
        if now - timestamp < CACHE_TTL:
            return status
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        status = member.status in ['member', 'creator', 'administrator']
    except:
        status = False
    _subscription_cache[user_id] = (status, now)
    return status

async def check_and_give_hourly_reward():
    while True:
        try:
            async with aiosqlite.connect('sqlite.db') as db:
                now = datetime.now()
                
                async with db.execute(
                    'SELECT user_id, is_subscribed FROM users WHERE hour_reward <= ?',
                    (now - timedelta(hours=1),)
                ) as cursor:
                    users = await cursor.fetchall()
                
                for user in users:
                    user_id = user[0]
                    real_subscription = await check_subscription_status(user_id)
                    reward = REWARD_SUBSCRIBED if real_subscription else REWARD_NON_SUBSCRIBED

                    if not real_subscription:
                        await db.execute(
                            'UPDATE users SET is_subscribed = 0 WHERE user_id = ?',
                            (user_id,)
                        )
                    
                    await db.execute(
                        'UPDATE users SET primogems = primogems + ?, hour_reward = ? WHERE user_id = ?',
                        (reward, now, user_id)
                    )
                
                await db.commit()
                
        except Exception as e:
            print(f"Ошибка в hourly_reward: {e}")
        
        await asyncio.sleep(3600)

async def refresh_subscription_status(user_id: int) -> bool:
    status = await check_subscription_status(user_id, force=True)
    async with aiosqlite.connect('sqlite.db') as db:
        await db.execute(
            'UPDATE users SET is_subscribed = ? WHERE user_id = ?',
            (1 if status else 0, user_id)
        )
        await db.commit()
    return status


async def start_hourly_reward():
    """Запускает фоновую задачу"""
    asyncio.create_task(check_and_give_hourly_reward())