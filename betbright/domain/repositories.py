from betbright.domain.entities import Sport
from betbright.framework.repository import BaseRepository


class SportRepository(BaseRepository):
    _model = Sport
