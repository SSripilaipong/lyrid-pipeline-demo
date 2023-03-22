from lyrid import Address
from lyrid.testing import CapturedMessage

from demo.core.page_loader import PageData
from demo.core.url_repo import GetUrl
from tests.page_loader.action import receive_url_data, page_loading_completed
from tests.page_loader.active.factory import create_active_page_loader


def test_should_get_next_url():
    url_repo = Address("$.tester.r")
    tester = create_active_page_loader(url_repo=url_repo)

    receive_url_data(tester)

    assert CapturedMessage(url_repo, GetUrl()) in tester.capture.get_messages()


def test_should_run_page_loading_background_task_when_receiving_url_data():
    tester = create_active_page_loader(load_page=_default_load_page)

    receive_url_data(tester, url="https://example.com/123")

    _assert_have_run_default_loading_background_task(tester, "https://example.com/123")


def test_should_not_run_new_page_loading_task_if_existing_task_is_not_completed_yet():
    url_repo = Address("$.tester.r")
    tester = create_active_page_loader(url_repo=url_repo)

    receive_url_data(tester)  # run one task first
    tester.capture.clear_background_tasks()

    receive_url_data(tester)

    assert len(tester.capture.get_background_tasks()) == 0


def test_should_run_new_page_loading_task_immediately_if_not_currently_loading_any_task():
    url_repo = Address("$.tester.r")
    tester = create_active_page_loader(url_repo=url_repo, load_page=_default_load_page)

    receive_url_data(tester)
    page_loading_completed(tester)
    tester.capture.clear_background_tasks()

    receive_url_data(tester, url="https://example.com/1")

    _assert_have_run_default_loading_background_task(tester, "https://example.com/1")


def _default_load_page(_: str) -> PageData: return PageData("", "")


def _assert_have_run_default_loading_background_task(tester, url):
    tasks = tester.capture.get_background_tasks()
    assert len(tasks) == 1
    task_call = tasks[0]
    assert task_call.task == _default_load_page and task_call.args == (url,)
