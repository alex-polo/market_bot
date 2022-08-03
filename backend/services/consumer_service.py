import asyncio

import aioredis
import redis

from config import RedisConfig


class ConsumerService:

    def __init__(self, redis_config: RedisConfig, t_delay=1) -> None:
        self.config = redis_config
        self.time_delay = t_delay
        self.status = False
        self.count = 0

    async def listener(self, message_handler):
        self.status = True
        redis = aioredis.from_url(
            "redis://89.108.103.38", port=6379, db=0, password='y3iuUyqW+H~M', encoding="utf-8", decode_responses=True
        )
        while self.status:
            # with redis.StrictRedis(
            #     host=self.config.hostname,
            #     port=self.config.port,
            #     password=self.config.password,
            #     db=self.config.database
            # ) as redis_client:
            #     redis_client.lpush('queue', self.count)
            try:
                pass
                async with redis.client() as conn:
                    await conn.lpush('queue', self.count)
                    self.count += 1
            except RuntimeError as error:
                # print(error)
                pass
            await asyncio.sleep(0.01)
