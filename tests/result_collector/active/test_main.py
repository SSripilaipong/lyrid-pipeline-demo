from lyrid.testing import CapturedMessage

from demo.core.result_collector import GetResult
from tests.result_collector.active.action import receive_result_data, saving_completed
from tests.result_collector.active.factory import create_active_result_collector, default_save
from tests.result_collector.active.util import random_result_data
from tests.result_collector.assertion import assert_have_run_saving_background_task
from tests.util import random_address


def test_should_save_results_when_result_are_fully_buffered():
    tester = create_active_result_collector(buffer_size=2, save=default_save)

    receive_result_data(tester, result_data=(result1 := random_result_data()))
    receive_result_data(tester, result_data=(result2 := random_result_data()))

    assert_have_run_saving_background_task(tester, default_save, [result1, result2])


def test_should_save_second_batch_without_the_first_batch():
    tester = create_active_result_collector(buffer_size=2, save=default_save)

    receive_result_data(tester)
    receive_result_data(tester)
    tester.capture.clear_background_tasks()
    saving_completed(tester)

    receive_result_data(tester, result_data=(result3 := random_result_data()))
    receive_result_data(tester, result_data=(result4 := random_result_data()))

    assert_have_run_saving_background_task(tester, default_save, [result3, result4])


def test_should_ask_for_result_from_processor_after_receiving_result():
    tester = create_active_result_collector(processors=[processor := random_address()])

    receive_result_data(tester, by=processor)

    assert CapturedMessage(receiver=processor, message=GetResult()) in tester.capture.get_messages()


def test_should_not_ask_for_result_from_other_processor():
    tester = create_active_result_collector(processors=[processor1 := random_address(), processor2 := random_address()])

    receive_result_data(tester, by=processor1)

    assert CapturedMessage(receiver=processor2, message=GetResult()) not in tester.capture.get_messages()


def test_should_not_ask_for_result_if_previous_saving_task_doesnt_finish():
    tester = create_active_result_collector(buffer_size=2)

    receive_result_data(tester)
    receive_result_data(tester)  # first saving task starts
    tester.capture.clear_background_tasks()

    receive_result_data(tester)
    receive_result_data(tester)
    assert tester.capture.get_background_tasks() == []


def test_should_save_results_after_saving_task_completed_if_the_results_are_full():
    tester = create_active_result_collector(buffer_size=2, save=default_save)

    receive_result_data(tester)
    receive_result_data(tester)  # first saving task starts

    receive_result_data(tester, result_data=(result3 := random_result_data()))
    receive_result_data(tester, result_data=(result4 := random_result_data()))
    tester.capture.clear_background_tasks()

    saving_completed(tester)

    assert_have_run_saving_background_task(tester, default_save, [result3, result4])
