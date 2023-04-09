from tests.result_collector.action import receive_result_data
from tests.result_collector.assertion import assert_have_run_saving_background_task
from tests.result_collector.factory import create_result_collector, default_save
from tests.result_collector.util import random_result_data


def test_should_save_results_when_result_are_fully_buffered():
    tester = create_result_collector(buffer_size=2, save=default_save)

    receive_result_data(tester, result_data=(result1 := random_result_data()))
    receive_result_data(tester, result_data=(result2 := random_result_data()))

    assert_have_run_saving_background_task(tester, default_save, [result1, result2])
