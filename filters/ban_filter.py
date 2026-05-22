from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from database import get_status


class IsNotBanned(BaseFilter):
    async def __call__(self, obj: Message | CallbackQuery) -> bool:
        if isinstance(obj, Message):
            user_id = obj.from_user.id
        elif isinstance(obj, CallbackQuery):
            user_id = obj.from_user.id
        else:
            return False

        status = await get_status(user_id)
        
        if status == 'banned':
            if isinstance(obj, CallbackQuery):
                await obj.answer("❌ Вы заблокированы и не можете использовать бота!", show_alert=True)
            return False
        
        return True
    
async def check_user_not_banned(user_id: int) -> bool:
    status = await get_status(user_id)
    return status != 'banned'