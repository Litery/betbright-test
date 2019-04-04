from betbright.domain.entities import Sport
from betbright.domain.serializers import DataclassSerializer

sport = Sport(None, 'sport 1', 'sport1', 'sport1', 5)
serializer = DataclassSerializer(Sport)

print(sport)
serialized = serializer.dump(sport)
print(serialized)

print(serializer.load(serialized))
