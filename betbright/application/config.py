from os import environ

from aioredis import Redis, create_redis_pool
from injector import Module

REDIS_URL = environ.get('REDIS_URL', 'redis://localhost')


class BaseModule(Module):
    async def setup_aio_providers(self, injector):
        redis = await create_redis_pool(
            REDIS_URL, minsize=5, maxsize=10)

        injector.binder.bind(Redis, to=redis)
