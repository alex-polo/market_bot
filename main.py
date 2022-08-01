import asyncio
from multiprocessing import Process

from loguru import logger

from config import Config
from tg_bot import start_tg_bot


async def worker_bg(pipe):

    while True:
        await asyncio.sleep(120)
        logger.warning('Background is await')


def _start_background(conf):
    asyncio.run(worker_bg(conf))


def start_main(config: Config):
    logger.debug('Start MAIN')

    tg_bot_process = Process(target=start_tg_bot, args=(
                                                        config.db_config,
                                                        config.redis_config,
                                                        config.tg_bot
                                                        ))
    tg_bot_process.start()

    background_process = Process(target=_start_background, args=(config.redis_config,))
    background_process.start()

    background_process.join()
