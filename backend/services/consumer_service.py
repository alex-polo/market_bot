import asyncio

import redis

from config import RedisConfig


class ConsumerService:

    def __init__(self, redis_config: RedisConfig, t_delay=1) -> None:
        self.redis_db = redis.StrictRedis(
            host=redis_config.hostname,
            port=redis_config.port,
            password=redis_config.password,
            db=redis_config.database
        )
        self.time_delay = t_delay
        self.status = False

    async def listener(self, message_handler):
        self.status = True
        while self.status:
            message = self.redis_db.get('event')
            message_handler(message)
            await asyncio.sleep(1)
