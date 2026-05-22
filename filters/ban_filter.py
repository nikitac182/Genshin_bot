from aiogram.filters import BaseFilter
from aiogram.types import Message
from database import get_status


class IsNotBanned(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        user_id = message.from_user.id

        status = await get_status(user_id)

        if status == 'banned':
            return False

        return True