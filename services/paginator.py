from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import COUNT_WISHES_PER_PAGE
from database import get_total_wishes

async def get_wish_menu_kb(
        page: int,
        max_page: int = None
    ) -> InlineKeyboardMarkup:

    if max_page == -1:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_menu")
                ],
            ]
        )
    elif page == 0:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="➡️", callback_data=f"next_wishes_{page}")
                ],
                [
                    InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_menu")
                ],
            ]
        )
    
    elif max_page is not None and page >= max_page:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="⬅️", callback_data=f"prev_wishes_{page}"),
                ],
                [
                    InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_menu")
                ],
            ]
        )
    elif page >= 1:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="⬅️", callback_data=f"prev_wishes_{page}"),
                    InlineKeyboardButton(text="➡️", callback_data=f"next_wishes_{page}")
                ],
                [
                    InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_menu")
                ],
            ]
        )
    

async def get_page(user_id: int, offset: int) -> int:
    """Получает номер страницы для пользователя"""
    return (offset // COUNT_WISHES_PER_PAGE) 

async def get_max_page(user_id: int, offset: int) -> int:
    """Получает номер последней страницы для пользователя"""
    total_wishes = await get_total_wishes(user_id)
    return (total_wishes - 1) // COUNT_WISHES_PER_PAGE