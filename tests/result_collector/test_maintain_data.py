from lyrid.testing import CapturedMessage

from demo.core.result_collector import GetResult
from tests.action import start
from tests.result_collector.active.action import receive_result_data
from tests.result_collector.idle.factory import create_idle_result_collector
from tests.util import random_address


def test_should_maintain_buffer_size_between_idle_state_and_active_state():
    tester = create_idle_result_collector(buffer_size=3)

    start(tester)  # become active
    receive_result_data(tester)
    receive_result_data(tester)
    assert len(tester.capture.get_background_tasks()) == 0  # should not start saving task until the third result

    receive_result_data(tester)
    assert len(tester.capture.get_background_tasks()) == 1


def test_should_maintain_processor_address_between_idle_state_and_active_state():
    tester = create_idle_result_collector(processor=(processor := random_address()))

    start(tester)  # become active
    tester.capture.clear_messages()

    receive_result_data(tester)
    assert CapturedMessage(processor, GetResult()) in tester.capture.get_messages()
