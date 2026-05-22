import asyncio
import aiosqlite
from datetime import datetime, timedelta

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
                    is_subscribed = user[1]

                    if is_subscribed:
                        reward = 150
                    else:
                        reward = 100
                    
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