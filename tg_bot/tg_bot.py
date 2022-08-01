import asyncio
import sqlite3

from loguru import logger
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from config import TgBot, DbConfig, RedisConfig
from tg_bot.filters import AdminFilter
from tg_bot.fsm.questionnaire import register_fsm_admin_questionnaire
from tg_bot.handlers import register_admin
# from tg_bot.handlers.fsm.fsm_questionnaire import register_fsm_admin_questionnaire
from tg_bot.services import UsersService
# from tg_bot.services.backend_consumer_service import BackendConsumer

mailing_service = None
# backed_consumer = None


def _create_users_service(db_connection: sqlite3.Connection, tg_bot_config: TgBot) -> UsersService:
    user_service = UsersService()
    user_service.set_parameters(db_connection, tg_bot_config.admin_ids)
    return user_service


def _register_filters(dispatcher: Dispatcher):
    dispatcher.filters_factory.bind(AdminFilter)


def _register_handlers(dispatcher: Dispatcher, users_service: UsersService):
    register_admin(dispatcher, users_service)
    # register_user(dispatcher, users_service)


def _register_fsm_questionnaire(dispatcher: Dispatcher):
    register_fsm_admin_questionnaire(dispatcher)


async def background_task(dispatcher: Dispatcher):
    while True:
        await asyncio.sleep(50)
        logger.info('Hello is background.')


async def run_background(dispatcher: Dispatcher):
    """Тут у нас запускается функция рассылки соообщений"""
    logger.debug('Telegram bot started')
    asyncio.create_task(background_task(dispatcher.bot))
    # asyncio.create_task(backed_consumer.listener())
    # asyncio.create_task(mailing_service.sending_message(background_queue))


def _shutdown():
    pass


def _main(db_config: DbConfig, redis_config: RedisConfig, tg_bot_config: TgBot):
    logger.debug('Starting telegram bot ...')
    logger.debug('Create memory storage')
    storage = MemoryStorage()

    logger.debug('Create telegram bot instance')
    bot = Bot(token=tg_bot_config.token)
    bot['admin_ids'] = tg_bot_config.admin_ids

    logger.debug('Create telegram bot dispatcher')
    dispatcher = Dispatcher(bot, storage=storage)

    logger.debug(f'Open database connection: {db_config.path}')
    db_connection = sqlite3.connect(db_config.path)

    logger.debug('Users Service creation')
    users_service = _create_users_service(db_connection=db_connection, tg_bot_config=tg_bot_config)

    # logger.debug('Mailing Service creation')
    # global mailing_service
    # mailing_service = MailingService(bot=bot, users_s=users_service, delay=1)

    # global backed_consumer
    # backed_consumer = BackendConsumer(redis_config=redis_config)

    logger.debug('Register filters tg_bot')
    _register_filters(dispatcher=dispatcher)

    logger.debug('Register FSM questionnaire')
    _register_fsm_questionnaire(dispatcher=dispatcher)

    logger.debug('Register handlers tg_bot')
    _register_handlers(dispatcher=dispatcher, users_service=users_service)

    executor.start_polling(dispatcher, skip_updates=True, on_startup=run_background)


def start_tg_bot(db_config: DbConfig, redis_config: RedisConfig, tg_bot_config: TgBot):
    _main(db_config=db_config, redis_config=redis_config, tg_bot_config=tg_bot_config)
