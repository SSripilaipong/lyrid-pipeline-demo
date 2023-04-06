from lyrid import Address
from lyrid.testing import CapturedMessage

from demo.core.page_loader import PageData
from tests.page_loader.action import receive_url_data, page_loading_completed
from tests.page_loader.empty.assertion import _assert_have_run_loading_background_task
from tests.page_loader.empty.factory import create_empty_page_loader, _default_load_page


def test_should_run_page_loading_background_task_when_receiving_url_data():
    tester = create_empty_page_loader(load_page=_default_load_page)

    receive_url_data(tester, url="https://example.com/123")

    _assert_have_run_loading_background_task(tester, _default_load_page, "https://example.com/123")


def test_should_send_loaded_page_to_an_existing_waiter_first():
    existing_waiter = Address("$.tester.me")
    tester = create_empty_page_loader(waiters=[existing_waiter])

    page_loading_completed(tester, page=PageData("https://example.com/1", "<html>Done!</html>"))

    assert CapturedMessage(
        existing_waiter, PageData("https://example.com/1", "<html>Done!</html>"),
    ) in tester.capture.get_messages()
