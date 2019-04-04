from unittest import TestCase

from betbright.domain.entities import EventType
from tests.utils import CommonScenario


class EntityTestCase(TestCase):
    def setUp(self):
        self.scenario = EntityTestCase.Scenario()

    def test_create_sport(self):
        scenario = self.scenario
        scenario.given_a_sport('sport 1')
        assert scenario.sport

    def test_create_event(self):
        scenario = self.scenario
        scenario \
            .given_a_sport('sport 1') \
            .given_an_event('event 1', EventType.PREPLAY, scenario.sport)

        assert scenario.event

    class Scenario(CommonScenario):
        pass
