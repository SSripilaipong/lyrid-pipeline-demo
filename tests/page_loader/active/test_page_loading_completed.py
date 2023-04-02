from lyrid import Address
from lyrid.testing import CapturedMessage

from demo.core.page_loader import PageData
from tests.page_loader.action import get_page, page_loading_completed, receive_url_data
from tests.page_loader.active.factory import create_active_page_loader


def test_should_send_loaded_page_to_an_existing_waiter_first():
    tester = create_active_page_loader()

    consumer = Address("$.tester.me")
    get_page(tester, sender=consumer)

    page_loading_completed(tester, page=PageData("https://example.com/1", "<html>Done!</html>"))

    assert CapturedMessage(
        consumer, PageData("https://example.com/1", "<html>Done!</html>"),
    ) in tester.capture.get_messages()


def test_should_load_new_page_loading_task_from_buffer_once_existing_task_is_completed():
    url_repo = Address("$.tester.r")
    tester = create_active_page_loader(url_repo=url_repo)

    receive_url_data(tester, url="https://example.com/1")
    first_task_id = tester.capture.get_background_tasks()[0].task_id
    receive_url_data(tester, url="https://example.com/2")
    tester.capture.clear_background_tasks()

    page_loading_completed(tester, task_id=first_task_id)

    assert len(tester.capture.get_background_tasks()) == 1
    assert tester.capture.get_background_tasks()[0].args[0] == "https://example.com/2"
