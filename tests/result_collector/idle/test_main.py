from demo.core import common
from demo.result_collector import ActiveResultCollector
from tests.result_collector.idle.factory import create_idle_result_collector
from tests.util import random_address


def test_should_become_active_after_start_message():
    tester = create_idle_result_collector()

    tester.simulate.tell(common.Start(), by=random_address())

    assert isinstance(tester.current_actor, ActiveResultCollector)
