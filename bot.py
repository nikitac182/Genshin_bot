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
from migrations import run_migrations 
    
bot = Bot(TOKEN)
dp = Dispatcher()


async def main():

    await run_migrations()

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

    await start_hourly_reward()
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())