import decimal
from dataclasses import dataclass
from enum import Enum


@dataclass
class Sport:
    id: int
    name: str
    display_name: str
    slug: str
    order: int


class EventType(Enum):
    PREPLAY = 'preplay'
    INPLAY = 'inplay'


class StatusType(Enum):
    PREPLAY = 'preplay'
    INPLAY = 'inplay'
    ENDED = 'ended'


@dataclass
class Event:
    name: str
    event_type: EventType
    sport: Sport
    status: StatusType
    slug: str
    active: bool = True


@dataclass
class Market:
    name: str
    display_name: str
    order: int
    schema: int
    columns: int


@dataclass
class Selection:
    name: str
    event: Event
    market: Market
    price: decimal
    order: int
    active: bool
    schema: int
    columns: int
