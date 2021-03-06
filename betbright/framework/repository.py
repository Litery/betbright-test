import logging
from itertools import zip_longest

from aioredis import Redis
from injector import inject

from betbright.domain.serializers import DataclassSerializer

logger = logging.getLogger()


class BaseRepository:
    _model = None

    @inject
    def __init__(self, connection: Redis, model=None):
        self.connection = connection
        self.model = model or self._model
        self.serializer = DataclassSerializer(self.model)

    @property
    def name(self):
        return

    async def get_unique_id(self):
        return await self.connection.incr(f'{self.model.__name__}:id')

    async def assign_id(self, entity):
        if entity.id:
            raise ValueError("Cannot insert existing entity or pre-set entity's id")
        entity.id = await self.get_unique_id()

    async def add(self, *entities):
        for entity in entities:
            await self.assign_id(entity)
        args = list(zip_longest(map(self.serializer.dump, entities), [], fillvalue=''))
        args = [item for sublist in args for item in sublist]
        if args:
            await self.connection.mset(args[0], args[1], *args[2:])

    async def delete(self, *entities):
        ids = [entity.id for entity in entities]
        matching = []
        for id in ids:
            async for key in self.connection.iscan(match=self.serializer.build_filter(id=id)):
                matching.append(key)
        if matching:
            await self.connection.unlink(matching[0], *matching[1:])

    async def get(self, **kwargs):
        pattern = self.serializer.build_filter(**kwargs)
        async for key in self.connection.iscan(match=pattern):
            yield self.serializer.load(key.decode('utf-8'))

    async def update(self, entity):
        await self.delete(entity)
        await self.add(entity)
