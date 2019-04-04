from aioredis import Redis
from injector import inject

from betbright.domain.entities import Sport, Event, Market, Selection
from betbright.domain.repositories import SportRepository, EventRepository, SelectionRepository, \
    MarketRepository


class UnitOfWork:
    @inject
    def __init__(self, redis: Redis):
        self.connection = redis
        self.repo_map = {
            Sport: self.sports,
            Event: self.events,
            Market: self.markets,
            Selection: self.selections
        }

    @property
    def sports(self) -> SportRepository:
        return SportRepository(self.connection)

    @property
    def events(self) -> EventRepository:
        return EventRepository(self.connection)

    @property
    def markets(self) -> MarketRepository:
        return MarketRepository(self.connection)

    @property
    def selections(self) -> SelectionRepository:
        return SelectionRepository(self.connection)
