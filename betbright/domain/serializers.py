import decimal

from betbright.domain.entities import StatusType, EventType


class DataclassSerializer:
    def __init__(self, model):
        self.model = model

    @staticmethod
    def _cast(_type, value):
        return None if value == 'None' else _type(value)

    def dump(self, obj):
        data = [self.model.__name__]
        attrs = self.model.__annotations__.keys()
        data += map(lambda attr: getattr(obj, attr), attrs)
        return ':'.join(map(str, data))

    def load(self, data):
        values = str(data).split(':')[1:]
        types = self.model.__annotations__.values()
        return self.model(*[self._cast(_type, value) for _type, value in zip(types, values)])

    def from_kwargs(self, **kwargs):
        for attr, _type in self.model.__annotations__.items():
            if kwargs[attr] and _type in (int, str, bytes, decimal.Decimal, StatusType, EventType):
                kwargs[attr] = self._cast(_type, kwargs[attr])
        return self.model(**kwargs)

    def build_filter(self, **kwargs):
        pattern = [self.model.__name__]
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        for key in self.model.__annotations__.keys():
            pattern.append(str(kwargs.get(key, '*')))
        return ':'.join(pattern)
