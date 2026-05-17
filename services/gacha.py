from aiogram.types import CallbackQuery, Message
from database import (
    get_pity,
    get_primogems,
    get_rarity,
    pull_pity,
    pull_rarity,
    pull_total_wishes,
    reduce_primogems
)
from utils import roll_rarity, update_pity


async def wish_one_time(
        user_id,
        target: CallbackQuery | Message
):
    pass

async def wish_ten_times(
    user_id,
    target: CallbackQuery | Message
):
    pass