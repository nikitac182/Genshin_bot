from aiogram import Router
from aiogram.types import CallbackQuery
from keyboards.inline import banner_menu_kb, menu_kb
from database import set_user_banner, get_user_banner

router = Router()

@router.callback_query(lambda c: c.data == 'change_banner')
async def change_banner_menu(call: CallbackQuery):
    current_banner = await get_user_banner(call.from_user.id)
    banner_names = {
    "characters": "Персонажи",
    "weapons": "Оружие", 
    "standard": "Стандартный"
    }
    banner_name = banner_names.get(current_banner, "Неизвестно")

    await call.message.edit_text(
        f"🔄 **Смена баннера**\n\n"
        f"Текущий баннер: **{banner_name}**\n\n"
        f"Выберите тип баннера для круток:",
        reply_markup=banner_menu_kb,
        parse_mode="Markdown"
    )
    await call.answer()

@router.callback_query(lambda c: c.data.startswith('banner_'))
async def set_banner(call: CallbackQuery):
    banner_type = call.data.split('_')[1]
    
    await set_user_banner(call.from_user.id, banner_type)
    
    banner_names_display = {
        "characters": "👥 Ивентовый",
        "weapons": "⚔️ Оружейный",
        "standard": "⭐ Стандартный"
    }
    
    banner_name = banner_names_display.get(banner_type, "Неизвестный")
    
    await call.message.edit_text(
        f"✅ Баннер сменён на **{banner_name}**!\n\n",
        reply_markup=menu_kb,
        parse_mode="Markdown"
    )
    await call.answer()

@router.callback_query(lambda c: c.data == 'back_to_menu')
async def back_to_menu(call: CallbackQuery):
    await call.message.edit_text("🏠 **Главное меню**", reply_markup=menu_kb, parse_mode="Markdown")
    await call.answer()