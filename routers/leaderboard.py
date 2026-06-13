import aiosqlite
import asyncio
import random
from aiogram.types import *
from aiogram import Router
from aiogram.fsm.context import FSMContext
from filters.ban_filter import IsNotBanned
from keyboards.inline import lb_back_kb, leaderboard_kb
from database import (
    get_users_for_leaderboard, 
    find_character_by_name, 
    get_users_for_character_leaderboard,
    get_user_rank_by_character,
    get_total_character_owners,
    find_weapon_by_name,
    get_users_for_weapon_leaderboard,
    get_user_weapon_rank,
    get_total_weapon_owners,
)
from state.leaderboard_state import *
from consts import WEAPON_ALIASES, CHARACTER_ALIASES
from utils1.randomizer import get_all_5star_characters, get_all_4star_characters

router = Router()
router.message.filter(IsNotBanned())
router.callback_query.filter(IsNotBanned())


@router.callback_query(lambda c: c.data == 'leaderboard')
async def set_leaderboard(call: CallbackQuery, state: FSMContext):
    await state.clear()
    user_id = call.from_user.id
    users = await get_users_for_leaderboard()

    async with aiosqlite.connect('sqlite.db') as db:
        async with db.execute('SELECT COUNT(*) FROM users') as cursor:
            total_users = await cursor.fetchone()
            total_users = total_users[0] if total_users else 0
        async with db.execute(
            'SELECT COUNT(*) + 1 FROM users WHERE total_wishes > (SELECT total_wishes FROM users WHERE user_id = ?)',
            (user_id,)
        ) as cursor:
            position = await cursor.fetchone()
            position = position[0] if position else '?'

    caption = f'🏆 <b>Топ игроков по круткам</b>:\n'
    i = 1
    for name, username, uid, total_wishes in users:
        username = f'@{username}'
        text = f'<a href="tg://user?id={uid}">{username if username else name}</a>'
        caption += f'\n{i}. {text} - {total_wishes} круток'
        i += 1
    caption += f'\n═══════════════\n📊 Ваша позиция: {position}/{total_users}'
    
    await call.message.edit_text(caption, reply_markup=leaderboard_kb, parse_mode='HTML')

@router.callback_query(lambda c: c.data == 'leaderboard_character')
async def leaderboard_character(call: CallbackQuery, state: FSMContext):
    msg = await call.message.edit_text(
        "🏆 **Введите имя персонажа**\n\n"
        "Различные сокращения также могут работать\n"
        "Примеры: Тао, Хайтам, Кофе",
        reply_markup=lb_back_kb,
        parse_mode='Markdown'
    )
    await state.update_data(bot_message_id=msg.message_id)
    await state.set_state(LeaderboardState.waiting_for_character)
    await call.answer()

@router.message(LeaderboardState.waiting_for_character)
async def leaderboard_name(message: Message, state: FSMContext):
    character_name = message.text.strip()
    if character_name.lower() == "хуйня":
        all_characters = get_all_5star_characters() * 5 + get_all_4star_characters()
        character_name = random.choice(all_characters)
    elif character_name.lower() in CHARACTER_ALIASES:
        character_name = CHARACTER_ALIASES[character_name.lower()]
    user_id = message.from_user.id
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    if bot_message_id:
        await message.bot.delete_message(chat_id=user_id, message_id=bot_message_id)
    await message.delete()
    matched_name = await find_character_by_name(character_name)

    if not matched_name:
        await message.answer(f"❌ Нет пользователей с персонажем {character_name}", reply_markup=lb_back_kb)
        await state.clear()
        return
    
    users = get_users_for_character_leaderboard(matched_name)
    user_rank = get_user_rank_by_character(user_id, matched_name)
    total_owners = get_total_character_owners(matched_name)
    users, user_rank, total_owners = await asyncio.gather(users, user_rank, total_owners)

    caption = f'🏆 <b>Топ по {matched_name}</b>:\n'
    i = 1
    for name, username, uid, constellation in users:
        username = f'@{username}'
        text = f'<a href="tg://user?id={uid}">{username if username else name}</a>'
        caption += f"\n{i}. {text} - C{constellation}"
        i += 1
    caption += f'\n═══════════════\n📊 Ваша позиция: {user_rank}/{total_owners}'
    await message.answer(caption, reply_markup=leaderboard_kb, parse_mode='HTML')
    await state.clear()

@router.callback_query(lambda c: c.data == 'leaderboard_weapon')
async def leaderboard_weapon(call: CallbackQuery, state: FSMContext):
    msg = await call.message.edit_text(
        "🏆 **Введите название оружия**\n\n"
        "Различные сокращения также могут работать\n"
        "Примеры: Хома, Аква, Ключ, Чайник",
        reply_markup=lb_back_kb,
        parse_mode='Markdown'
    )
    await state.update_data(bot_message_id=msg.message_id)
    await state.set_state(LeaderboardState.waiting_for_weapon)
    await call.answer()


@router.message(LeaderboardState.waiting_for_weapon)
async def leaderboard_weapon_name(message: Message, state: FSMContext):
    weapon_name = message.text.strip()
    if weapon_name.lower() in WEAPON_ALIASES:
        weapon_name = WEAPON_ALIASES[weapon_name.lower()]
    user_id = message.from_user.id
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    if bot_message_id:
        await message.bot.delete_message(chat_id=user_id, message_id=bot_message_id)
    await message.delete()
    matched_name = await find_weapon_by_name(weapon_name)

    if not matched_name:
        await message.answer(f"❌ Нет пользователей с оружием {weapon_name}", reply_markup=lb_back_kb)
        await state.clear()
        return
    
    users = get_users_for_weapon_leaderboard(matched_name)
    user_rank = get_user_weapon_rank(user_id, matched_name)
    total_owners = get_total_weapon_owners(matched_name)
    users, user_rank, total_owners = await asyncio.gather(users, user_rank, total_owners)
    
    caption = f'🏆 <b>Топ по {matched_name}</b>:\n'
    i = 1
    for name, username, uid, refinement in users:
        username = f'@{username}'
        text = f'<a href="tg://user?id={uid}">{username if username else name}</a>'
        caption += f"\n{i}. {text} - R{refinement}"
        i += 1
    
    caption += f'\n═══════════════\n📊 Ваша позиция: {user_rank}/{total_owners}'
    
    await message.answer(caption, reply_markup=leaderboard_kb, parse_mode='HTML')
    await state.clear()