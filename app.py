from multiprocessing import Process

from loguru import logger

import backend
import tg_bot
from config import Config


def start_main(config: Config):
    logger.debug('Start MAIN')

    tg_bot_process = Process(target=tg_bot.run, args=(
                                                        config.db_config,
                                                        config.redis_config,
                                                        config.tg_bot
                                                        ))
    tg_bot_process.start()

    backend_process = Process(target=backend.run, args=(config.redis_config,))
    backend_process.start()

    tg_bot_process.join()
    # backend_process.join()
