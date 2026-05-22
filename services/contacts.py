from aiogram.types import CallbackQuery
from config import ADMIN_USERNAME
from consts import CONTACT_ADMIN_MESSAGE
from keyboards.inline import back_menu_kb


async def contact_admin(call: CallbackQuery):
    await call.message.edit_text(
        CONTACT_ADMIN_MESSAGE.format(admin_username='\n'.join(ADMIN_USERNAME)),
        reply_markup=back_menu_kb
    )