from aioredis import Redis
from injector import inject


class BaseRepository:
    @inject
    def __init__(self, connection: Redis):
        self.connection = connection

    async def add(self, entity):
        pass

    async def delete(self, entity):
        pass

    async def get(self, **kwargs):
        pass

    async def update(self, entity):
        pass
