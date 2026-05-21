from aiogram.types import CallbackQuery, Message
from config import ADMIN_ID
from utils import roll_rarity, update_pity
from state.payment_state import PaymentState
from aiogram.fsm.context import FSMContext
from keyboards.inline import payment_confirm_kb
from consts import PAYMENT_INSTRUCTION, TOPUP_REQUEST


async def process_buy(call: CallbackQuery, state: FSMContext):
    primogems = int(call.data.split('_')[1])
    price = int(call.data.split('_')[2])

    await state.set_state(PaymentState.waiting_for_payment)
    await state.update_data(primogems=primogems, price=price)

    await call.message.edit_text(
        PAYMENT_INSTRUCTION.format(amount=price),
        reply_markup=payment_confirm_kb
    )

async def confirm_payment(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    primogems = data.get('primogems')
    price = data.get('price')

    await call.bot.send_message(
        ADMIN_ID,
        TOPUP_REQUEST.format(
            user_id=call.from_user.id,
            username=call.from_user.username,
            amount=price,
            primogems=primogems
        )
    )