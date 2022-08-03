import asyncio
from loguru import logger

from backend.services import ConsumerService
from config import RedisConfig


def _message_handler(message):
    logger.info(message)


async def _main(redis_config: RedisConfig):
    consumer = ConsumerService(redis_config=redis_config)
    await consumer.listener(_message_handler)


def run(redis_config: RedisConfig):
    asyncio.run(_main(redis_config=redis_config))
