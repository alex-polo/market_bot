import typing

from aiogram.dispatcher.filters import BoundFilter


class AdminFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin: typing.Optional[bool] = None) -> None:
        self.is_admin = is_admin

    async def check(self, obj) -> bool:
        if self.is_admin is None:
            return False
        return (obj.from_user.id in obj.bot.get('admin_ids')) == self.is_admin
