from lyrid import Address
from lyrid.testing import CapturedMessage

from demo.core.url_repo import GetUrl
from tests.page_loader.action import receive_url_data
from tests.page_loader.active.factory import create_active_page_loader


def test_should_get_next_url():
    url_repo = Address("$.tester.r")
    tester = create_active_page_loader(url_repo=url_repo)

    receive_url_data(tester)

    assert CapturedMessage(url_repo, GetUrl()) in tester.capture.get_messages()


def test_should_run_page_loading_background_task_when_receiving_url_data():
    def load_page(_: str) -> str: return ""

    tester = create_active_page_loader(load_page=load_page)

    receive_url_data(tester, url="https://example.com/123")

    tasks = tester.capture.get_background_tasks()
    assert len(tasks) == 1
    task_call = tasks[0]

    assert task_call.task == load_page and task_call.args == ("https://example.com/123",)


def test_should_not_run_new_page_loading_task_if_existing_task_is_not_completed_yet():
    url_repo = Address("$.tester.r")
    tester = create_active_page_loader(url_repo=url_repo)

    receive_url_data(tester)  # run one task first
    tester.capture.clear_background_tasks()

    receive_url_data(tester)

    assert len(tester.capture.get_background_tasks()) == 0
