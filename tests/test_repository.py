from aioredis import Redis
from asynctest import TestCase, asyncio

from injector import Injector

from betbright.application.config import BaseModule
from betbright.domain.repositories import SportRepository
from betbright.framework.repository import BaseRepository
from tests.utils import CommonScenario


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
        await self.connection.wait_closed()

    async def test_connection(self):
        await self.connection.set('test key', 'test value')
        assert b'test value' == await self.connection.get('test key')

    async def test_connection_2(self):
        await self.connection.set('test key', 'test value')
        await self.connection.set('test key 2', 'test value 2')
        assert b'test value' == await self.connection.get('test key')
        assert b'test value 2' == await self.connection.get('test key 2')


class SportRepoTestCase(ConnectionTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scenario: SportRepoTestCase.Scenario = None

    async def setUp(self):
        await super().setUp()
        self.scenario = SportRepoTestCase.Scenario()
        self.scenario.repository = self.injector.get(SportRepository)
        self.scenario.connection = self.injector.get(Redis)

    async def test_getting_unique_id(self):
        scenario = self.scenario

        async def get_id(repo: BaseRepository, _list):
            _list += [await repo.get_unique_id()]

        results = []
        await asyncio.gather(*[get_id(scenario.repository, results) for _ in range(15)])
        for x, y in zip(sorted(results), range(1, 16)):
            assert x == y

    async def test_add_multiple_sports(self):
        scenario = self.scenario
        scenario \
            .given_a_sport('sport 1') \
            .given_a_sport('sport 2') \
            .given_a_sport('sport 3')

        await scenario.when_i_populate_db_with_data()
        await scenario.then_the_number_of_sports_should_be(3)

    async def test_delete_multiple_sports(self):
        scenario = self.scenario
        scenario \
            .given_a_sport('sport 1') \
            .given_a_sport('sport 2') \
            .given_a_sport('sport 3')

        await scenario.when_i_populate_db_with_data()
        await scenario.then_the_number_of_sports_should_be(3)
        await scenario.when_i_delete_sports(scenario.sports[:2])
        await scenario.then_the_number_of_sports_should_be(1)

    class Scenario(CommonScenario):
        def __init__(self):
            super().__init__()
            self.repository: SportRepository = None
            self.connection = None

        async def when_i_populate_db_with_data(self):
            for model, entity_list in self.entities.items():
                repo = BaseRepository(self.connection, model)
                await repo.add(*entity_list)

        async def then_the_number_of_sports_should_be(self, n):
            self.results = []
            async for sport in self.repository.get():
                self.results.append(sport)
            print(self.results)
            assert len(self.results) == n

        async def when_i_delete_sports(self, sports):
            await self.repository.delete(*sports)
