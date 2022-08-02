import asyncio
from loguru import logger

from backend.services import ConsumerService
from config import RedisConfig


def _message_handler(message):
    logger.info(message)


async def _main(redis_config: RedisConfig):
    consumer = ConsumerService(redis_config=redis_config)
    # asyncio.create_task(consumer.listener(_message_handler))
    await consumer.listener(_message_handler)
    print(11111111111111111111111111)


def run(redis_config: RedisConfig):
    asyncio.run(_main(redis_config=redis_config))
