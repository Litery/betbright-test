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

    def build_filter(self, **kwargs):
        pattern = [self.model.__name__]
        for key in self.model.__annotations__.keys():
            pattern.append(kwargs.get(key, '*'))
        return ':'.join(pattern)
