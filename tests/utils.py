import decimal
from typing import List

from betbright.domain.entities import Sport, Event, Market, Selection, EventType, StatusType


class CommonScenario:
    def __init__(self):
        self.result = None
        self.results = []
        self.sport: Sport = None
        self.sports: List[Sport] = []
        self.event: Event = None
        self.events: List[Event] = []
        self.market: Market = None
        self.markets: List[Market] = []
        self.selection: Selection = None
        self.selections: List[Selection] = []
        self.entities = {
            Sport: self.sports,
            Event: self.events,
            Market: self.markets,
            Selection: self.selections
        }

    def _create_entity(self, cls, *args, **kwargs):
        instance = cls(*args, **kwargs)
        name = cls.__name__.lower()
        setattr(self, name, instance)
        _list = getattr(self, f'{name}s')
        _list.append(instance)

    def given_a_sport(self, name: str, _id: int = None, order=0):
        args = _id, name, name.title(), name.replace(' ', ''), order
        self._create_entity(Sport, *args)
        return self

    def given_an_event(self, name: str, event_type: EventType, sport: Sport = None,
                       status: StatusType = None, _id: int = None):
        args = _id, name, event_type, sport or self.sport, status, name.replace(' ', '')
        self._create_entity(Event, *args)
        return self

    def given_a_market(self, name: str, order: int, schema: int, columns: int, _id: int = None):
        args = _id, name, name.title(), order, schema, columns
        self._create_entity(Market, *args)
        return self

    def given_a_selection(self, name: str, price: decimal, order: int, schema: int, columns: int,
                          event: Event = None, market: Market = None,
                          active: bool = True, _id: int = None):
        args = (_id, name, event or self.event, market or self.market, price, order, active,
                schema, columns)
        self._create_entity(Selection, *args)
        return self

    def result_should_equal_to(self, expected):
        assert expected == self.result
        return self
