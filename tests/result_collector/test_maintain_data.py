from lyrid.testing import CapturedMessage

from demo.core.result_collector import GetResult
from tests.action import start
from tests.result_collector.active.action import receive_result_data
from tests.result_collector.active.factory import default_save
from tests.result_collector.active.util import random_result_data
from tests.result_collector.assertion import assert_have_run_saving_background_task
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
    tester = create_idle_result_collector(processors=[processor := random_address()])

    start(tester)  # become active
    tester.capture.clear_messages()

    receive_result_data(tester, by=processor)
    assert CapturedMessage(processor, GetResult()) in tester.capture.get_messages()


def test_should_maintain_saving_task_between_idle_state_and_active_state():
    tester = create_idle_result_collector(buffer_size=1, save=default_save)

    start(tester)  # become active
    tester.capture.clear_messages()

    receive_result_data(tester, result_data=(result1 := random_result_data()))
    assert_have_run_saving_background_task(tester, default_save, [result1])
