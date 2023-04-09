from demo.core import common
from tests.result_collector.active.action import receive_result_data
from tests.result_collector.idle.factory import create_idle_result_collector
from tests.util import random_address


def test_should_maintain_buffer_size_between_idle_state_and_active_state():
    tester = create_idle_result_collector(buffer_size=3)

    tester.simulate.tell(common.Start(), by=random_address())  # become active
    receive_result_data(tester)
    receive_result_data(tester)
    assert len(tester.capture.get_background_tasks()) == 0  # should not start saving task until the third result

    receive_result_data(tester)
    assert len(tester.capture.get_background_tasks()) == 1
