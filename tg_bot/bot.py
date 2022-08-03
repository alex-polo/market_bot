import asyncio
import sqlite3

import aioredis
from loguru import logger
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from config import TgBot, DbConfig, RedisConfig
from tg_bot.filters import AdminFilter
from tg_bot.fsm.questionnaire import register_fsm_admin_questionnaire
from tg_bot.handlers import register_admin
from tg_bot.services import UsersService

mailing_service = None
r_config = None


def _create_users_service(db_connection: sqlite3.Connection, tg_bot_config: TgBot) -> UsersService:
    user_service = UsersService()
    user_service.set_parameters(db_connection, tg_bot_config.admin_ids)
    return user_service


def _register_filters(dispatcher: Dispatcher):
    logger.info('Register filters tg_bot')
    dispatcher.filters_factory.bind(AdminFilter)


def _register_handlers(dispatcher: Dispatcher, users_service: UsersService):
    logger.info('Register handlers tg_bot')
    register_admin(dispatcher, users_service)
    # register_user(dispatcher, users_service)


def _register_fsm_questionnaire(dispatcher: Dispatcher, users_service: UsersService):
    logger.info('Register FSM questionnaire')
    register_fsm_admin_questionnaire(dispatcher, users_service)


async def background_task(dispatcher: Dispatcher):
    redis = aioredis.from_url(
        "redis://89.108.103.38", port=6379, db=0, password='y3iuUyqW+H~M', encoding="utf-8", decode_responses=True
    )

    while True:
        async with redis.client() as conn:
            _, message = await conn.brpop("queue")
            logger.info(message)
        # try:
        #     async with redis.client() as conn:
        #         _, message = await conn.brpop("queue")
        #         logger.info(message)
        # except RuntimeError as error:
        #     print(error)


async def run_background(dispatcher: Dispatcher):
    """Тут у нас запускается функция рассылки соообщений"""
    logger.debug('Telegram bot started')
    asyncio.create_task(background_task(dispatcher.bot))
    # asyncio.create_task(backed_consumer.listener())


def _main(db_config: DbConfig, redis_config: RedisConfig, tg_bot_config: TgBot):
    logger.info('Starting telegram bot ...')
    logger.info('Create memory storage')
    storage = MemoryStorage()

    logger.info('Create telegram bot instance')
    bot = Bot(token=tg_bot_config.token)
    bot['admin_ids'] = tg_bot_config.admin_ids

    logger.info('Create telegram bot dispatcher')
    dispatcher = Dispatcher(bot, storage=storage)

    logger.info(f'Open database connection: {db_config.path}')
    db_connection = sqlite3.connect(db_config.path)

    logger.info('Users Service creation')
    users_service = _create_users_service(db_connection=db_connection, tg_bot_config=tg_bot_config)

    # asyncio.Step
    # logger.debug('Mailing Service creation')
    # global mailing_service
    # mailing_service = MailingService(bot=bot, users_s=users_service, delay=1)

    global r_config
    r_config = redis_config

    _register_filters(dispatcher=dispatcher)
    _register_fsm_questionnaire(dispatcher=dispatcher, users_service=users_service)
    _register_handlers(dispatcher=dispatcher, users_service=users_service)

    executor.start_polling(dispatcher=dispatcher, skip_updates=True, on_startup=run_background)


def run(db_config: DbConfig, redis_config: RedisConfig, tg_bot_config: TgBot):
    _main(db_config=db_config, redis_config=redis_config, tg_bot_config=tg_bot_config)
