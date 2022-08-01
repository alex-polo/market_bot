import sqlite3

from aiogram import Dispatcher
from aiogram.types import Message, ReplyKeyboardRemove

from tg_bot.services import UsersService

user_service = None


async def user_command_start(message: Message):
    user_service.adding_user_or_set_active_status(message.from_user)

    await message.reply(f'Hello {message.from_user.full_name}.\n'
                        f'You id: {message.from_user.id}')


async def user_command_help(message: Message):
    await message.reply(f'Hello {message.from_user.full_name}.\n'
                        f'I am Mugen.\n'
                        f'You id: {message.from_user.id}.', reply_markup=ReplyKeyboardRemove())


async def view_subscribe(message: Message):
    await message.reply('У вас пока нет подписок')


async def user_command_unknown(message: Message):
    await message.answer('Unknown commander.')


def register_user(dp: Dispatcher, users_service: UsersService):
    dp.register_message_handler(user_command_start, commands=["start"], state="*")
    dp.register_message_handler(user_command_help, commands=["help"], state="*")
    dp.register_message_handler(view_subscribe, commands=["view_settings"], state="*")
    dp.register_message_handler(user_command_unknown, state="*")

    global user_service
    user_service = users_service
