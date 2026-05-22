from aiogram.types import CallbackQuery, Message
from config import ADMIN_ID
from utils import roll_rarity, update_pity
from state.payment_state import PaymentState
from aiogram.fsm.context import FSMContext
from keyboards.inline import payment_confirm_kb, confirm_payment_kb
from consts import PAYMENT_CONFIRMED_TEXT, PAYMENT_INSTRUCTION, PAYMENT_REQUEST_SENT_TEXT, TOPUP_REQUEST
from database import add_primogems


async def process_buy(call: CallbackQuery, state: FSMContext):
    primogems = int(call.data.split('_')[1])
    price = int(call.data.split('_')[2])
    user_id = call.from_user.id
    username = call.from_user.username
    await state.set_state(PaymentState.waiting_for_payment)
    await state.update_data(
        primogems=primogems,
        price=price,
        user_id=user_id,
        username=username
    )

    await call.message.edit_text(
        PAYMENT_INSTRUCTION.format(amount=price),
        reply_markup=payment_confirm_kb
    )

async def confirm_payment(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    primogems = data.get('primogems')
    price = data.get('price')
    user_id = data.get('user_id')
    username = data.get('username')
    for admin_id in ADMIN_ID:
        await call.bot.send_message(
            admin_id,
            TOPUP_REQUEST.format(
                user_id=user_id,
                username=username,
                amount=price,
                primogems=primogems
            ),
            reply_markup=confirm_payment_kb
        )
    await call.message.edit_text(PAYMENT_REQUEST_SENT_TEXT)

async def admin_confirm_payment(call: CallbackQuery, state: FSMContext):
    # Здесь должна быть логика подтверждения платежа администратором
    # Например, можно извлечь информацию о платеже из текста сообщения
    # и обновить баланс пользователя в базе данных
    data = await state.get_data()
    user_id = data.get('user_id')
    username = data.get('username')
    primogems = data.get('primogems')
    await add_primogems(user_id, primogems)
    await call.message.edit_text(
        PAYMENT_CONFIRMED_TEXT.format(username=username, amount=primogems)
    )