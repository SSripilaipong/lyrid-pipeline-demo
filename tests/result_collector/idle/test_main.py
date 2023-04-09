from lyrid.testing import CapturedMessage

from demo.core.result_collector import GetResult
from demo.result_collector import ActiveResultCollector
from tests.action import start
from tests.result_collector.idle.factory import create_idle_result_collector
from tests.util import random_address


def test_should_become_active_after_start_message():
    tester = create_idle_result_collector()

    start(tester)

    assert isinstance(tester.current_actor, ActiveResultCollector)


def test_should_ask_for_result_from_processor():
    tester = create_idle_result_collector(processor=(processor := random_address()))

    start(tester)

    assert CapturedMessage(processor, GetResult()) in tester.capture.get_messages()
