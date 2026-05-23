from aiogram.types import *
from aiogram import Router
from aiogram.fsm.context import FSMContext
from config import COUNT_WISHES_PER_PAGE
from consts import LAST
from filters.ban_filter import IsNotBanned
from keyboards.inline import menu_kb
from services.user_profile import process_promo_code, set_promo_code, set_story_wishes, set_profile
from state.promocode_state import PromoState

router = Router()
router.message.filter(IsNotBanned())
router.callback_query.filter(IsNotBanned())


@router.callback_query(lambda c: c.data == 'profile')
async def handler_set_profile(call: CallbackQuery):
    if int(call.from_user.id) != int(call.data.split('_')[1]):
        call.answer()
        return
    await set_profile(call)

@router.callback_query(lambda c: c.data == 'story_wishes')
async def handler_set_story_wishes(call: CallbackQuery):
    await set_story_wishes(call)

@router.callback_query(lambda c: c.data == 'back_to_menu_from_profile')
async def back_to_menu_from_profile(call: CallbackQuery):
    await call.message.edit_text('Главное меню', reply_markup=menu_kb)

@router.callback_query(lambda c: c.data.startswith('prev_wishes_'))
async def prev_wishes(call: CallbackQuery):
    page = int(call.data.split('_')[LAST])
    offset = (page - 1) * COUNT_WISHES_PER_PAGE
    await set_story_wishes(
        call,
        offset=offset
    )
    
@router.callback_query(lambda c: c.data.startswith('next_wishes_'))
async def next_wishes(call: CallbackQuery):
    page = int(call.data.split('_')[LAST])
    offset = (page + 1) * COUNT_WISHES_PER_PAGE
    await set_story_wishes(
        call,
        offset=offset
    )

@router.callback_query(lambda c: c.data == 'promo_code')
async def handle_promo_code(call: CallbackQuery, state: FSMContext):
    await set_promo_code(call, state)

@router.message(PromoState.waiting_for_promo_code)
async def handle_process_promo_code(message: Message, state: FSMContext):
    await process_promo_code(message, state)
    await state.clear()
