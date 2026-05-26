import asyncio
import aiosqlite
from datetime import datetime, timedelta
from aiogram import Bot
from config import TOKEN, REWARD_NON_SUBSCRIBED, REWARD_SUBSCRIBED, CHANNEL_ID

bot = Bot(token=TOKEN)

async def check_subscription_status(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ['member', 'creator', 'administrator']
    except:
        return False

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

                    if real_subscription:
                        reward = REWARD_SUBSCRIBED
                    else:
                        reward = REWARD_NON_SUBSCRIBED
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


async def start_hourly_reward():
    """Запускает фоновую задачу"""
    asyncio.create_task(check_and_give_hourly_reward())