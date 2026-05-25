import os
import asyncio
import requests
from flask import Flask, request, jsonify
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from dotenv import load_dotenv
from routers.admin import router as admin_router
from routers.start import router as start_router
from routers.wishes import router as wishes_router
from routers.profile import router as profile_router
from routers.shop import router as shop_router
from routers.leaderboard import router as leaderboard_router
from routers.banners import router as banner_router
from routers.exchange import router as exchange_router
from routers.group_start import router as group_router
from routers.subscription import router as subscription_router
from migrations import run_migrations

load_dotenv()
BOT_TOKEN = os.getenv('TOKEN')
WEBHOOK_URL = 'https://Sshkotik.pythonanywhere.com/webhook'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

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

app = Flask(__name__)

@app.route('/')
def index():
    return 'Genshin Gacha Bot is running!', 200

@app.route('/webhook', methods=['POST'])
async def webhook():
    try:
        update = Update(**request.json)
        await dp.feed_update(bot, update)
        return jsonify({'status': 'ok'}), 200
    except Exception as e:
        print(f"Ошибка: {e}")
        return jsonify({'status': 'error'}), 500

@app.route('/setup', methods=['GET'])
def setup():
    try:
        asyncio.run(run_migrations())
        url = WEBHOOK_URL
        response = requests.post(
            f'https://api.telegram.org/bot{BOT_TOKEN}/setWebhook',
            data={'url': url}
        )
        return jsonify({
            'status': 'ok',
            'migrations': 'done',
            'webhook': response.json()
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'alive'}), 200