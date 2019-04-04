from aioredis import Redis
from asynctest import TestCase

from injector import Injector

from betbright.application.config import BaseModule


class ConnectionTestCase(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.injector = Injector()
        self.connection = None

    async def setUp(self):
        module = BaseModule()
        await module.setup_aio_providers(self.injector)
        self.injector.binder.install(module)
        self.connection = self.injector.get(Redis)

    async def tearDown(self):
        await self.connection.flushall()
        self.connection.close()

    async def test_connection(self):
        await self.connection.set('test key', 'test value')
        assert b'test value' == await self.connection.get('test key')

    async def test_connection_2(self):
        await self.connection.set('test key', 'test value')
        await self.connection.set('test key 2', 'test value 2')
        assert b'test value' == await self.connection.get('test key')
        assert b'test value 2' == await self.connection.get('test key 2')
