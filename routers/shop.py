from aiogram.types import CallbackQuery
from aiogram import Router
from filters.ban_filter import IsNotBanned
from keyboards.inline import shop_menu_kb
from services.payments import confirm_payment, process_buy
from services.contacts import contact_admin
from aiogram.fsm.context import FSMContext
from services.payments import admin_confirm_payment

router = Router()
router.message.filter(IsNotBanned())


@router.callback_query(lambda c: c.data == 'primogems_buy')
async def buy_primogems(call: CallbackQuery):
    await call.message.edit_text('Купить примогемы.', reply_markup=shop_menu_kb)

@router.callback_query(lambda c: c.data == 'contact_admin')
async def handle_contact_admin(call: CallbackQuery):
    await contact_admin(call)
    
@router.callback_query(lambda c: c.data.startswith('buy_'))
async def handle_process_buy(call: CallbackQuery, state: FSMContext):
    await process_buy(call, state)

@router.callback_query(lambda c: c.data == 'confirm_payment')
async def handle_confirm_payment(call: CallbackQuery, state: FSMContext):
    await confirm_payment(call, state)

@router.callback_query(lambda c: c.data == 'cancel_payment')
async def handle_cancel_payment(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await buy_primogems(call)

@router.callback_query(lambda c: c.data == 'admin_confirm_payment')
async def handle_admin_confirm_payment(call: CallbackQuery, state: FSMContext):
    await admin_confirm_payment(call, state)
    await state.clear()

@router.callback_query(lambda c: c.data == 'admin_cancel_payment')
async def handle_admin_cancel_payment(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await buy_primogems(call)