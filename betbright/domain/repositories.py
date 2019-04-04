from betbright.domain.entities import Sport, Event, Market, Selection
from betbright.framework.repository import BaseRepository


class SportRepository(BaseRepository):
    _model = Sport


class EventRepository(BaseRepository):
    _model = Event


class MarketRepository(BaseRepository):
    _model = Market


class SelectionRepository(BaseRepository):
    _model = Selection
