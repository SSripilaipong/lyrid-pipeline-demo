from lyrid.testing import CapturedMessage

from demo.core.result_collector import GetResult
from tests.result_collector.active.action import receive_result_data, saving_completed
from tests.result_collector.active.assertion import assert_have_run_saving_background_task
from tests.result_collector.active.factory import create_result_collector, default_save
from tests.result_collector.active.util import random_result_data
from tests.util import random_address


def test_should_save_results_when_result_are_fully_buffered():
    tester = create_result_collector(buffer_size=2, save=default_save)

    receive_result_data(tester, result_data=(result1 := random_result_data()))
    receive_result_data(tester, result_data=(result2 := random_result_data()))

    assert_have_run_saving_background_task(tester, default_save, [result1, result2])


def test_should_save_second_batch_without_the_first_batch():
    tester = create_result_collector(buffer_size=2, save=default_save)

    receive_result_data(tester)
    receive_result_data(tester)
    tester.capture.clear_background_tasks()
    saving_completed(tester)

    receive_result_data(tester, result_data=(result3 := random_result_data()))
    receive_result_data(tester, result_data=(result4 := random_result_data()))

    assert_have_run_saving_background_task(tester, default_save, [result3, result4])


def test_should_ask_for_result_from_processor_after_receiving_result():
    tester = create_result_collector(processor=(processor := random_address()))

    receive_result_data(tester)

    assert CapturedMessage(receiver=processor, message=GetResult()) in tester.capture.get_messages()
