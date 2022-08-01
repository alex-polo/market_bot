from aiogram import Dispatcher
from aiogram.types import Message

from tg_bot.services import UsersService

users_service = None


async def admin_start(message: Message):
    users_service.adding_user_or_set_active_status(message.from_user)
    await message.reply("Hi, master!")


async def admin_help(message: Message):
    await message.answer(f'Help:\n'
                         f'/subscription - управление подписками\n'
                         f'/clear - удалить все подписки.\n'
                         f'/views_count_user \n'
                         f'/view_user \n'
                         f'/stop_subscription \n'
                         f'/start_subscription\n')


async def views_count_user(message: Message):
    await message.reply("This is views_count_user master.")


async def view_user(message: Message):
    await message.reply("This is view_user master.")


async def admin_command_unknown(message: Message):
    await message.answer('Unknown command master.')


def register_admin(dp: Dispatcher, users_s: UsersService):
    global users_service
    users_service = users_s

    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
    dp.register_message_handler(admin_help, commands=["help"], state="*", is_admin=True)
    dp.register_message_handler(views_count_user, commands=["views_count_user"], state="*", is_admin=True)
    dp.register_message_handler(view_user, commands=["view_user"], state="*", is_admin=True)
    dp.register_message_handler(admin_command_unknown, state="*", is_admin=True)
