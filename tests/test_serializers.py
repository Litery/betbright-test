from unittest import TestCase

from betbright.domain.entities import Sport
from betbright.domain.serializers import DataclassSerializer
from tests.utils import CommonScenario


class SportSerializerTestCase(TestCase):
    def setUp(self):
        self.scenario = SportSerializerTestCase.Scenario()
        self.serializer = DataclassSerializer(Sport)

    def test_dump(self):
        scenario = self.scenario
        scenario \
            .given_a_sport('sport 1', 1) \
            .given_a_sport('sport 2', 2) \
            .when_i_dump_a_sport(scenario.sports[0]) \
            .result_should_equal_to('Sport:1:sport 1:Sport 1:sport1:0') \
            .when_i_dump_a_sport(scenario.sports[1]) \
            .result_should_equal_to('Sport:2:sport 2:Sport 2:sport2:0')

    def test_load(self):
        scenario = self.scenario
        scenario \
            .given_a_sport('sport 1', 1) \
            .when_i_load_data('Sport:1:sport 1:Sport 1:sport1:0') \
            .result_should_equal_to(scenario.sport)

    def test_dump_and_load(self):
        scenario = self.scenario
        scenario \
            .given_a_sport('sport 1') \
            .when_i_dump_a_sport() \
            .when_i_load_data(scenario.result) \
            .result_should_equal_to(scenario.sport)

    class Scenario(CommonScenario):
        def __init__(self):
            super().__init__()
            self.serializer = DataclassSerializer(Sport)

        def when_i_dump_a_sport(self, sport=None):
            self.result = self.serializer.dump(sport or self.sport)
            return self

        def when_i_load_data(self, data):
            self.result = self.serializer.load(data)
            return self
