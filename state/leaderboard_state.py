from aiogram.fsm.state import State, StatesGroup

class LeaderboardState(StatesGroup):
    waiting_for_character = State()
    waiting_for_weapon = State()