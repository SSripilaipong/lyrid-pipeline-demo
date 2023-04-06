from lyrid.testing import CapturedMessage

from tests.page_loader.action import receive_url_data, page_loading_completed, get_page
from tests.page_loader.empty.assertion import _assert_have_run_loading_background_task
from tests.page_loader.empty.factory import create_empty_page_loader
from tests.page_loader.factory import _default_load_page
from tests.page_loader.util import random_page_data
from tests.util import random_address, random_url


def test_should_run_page_loading_background_task_when_receiving_url_data():
    tester = create_empty_page_loader(load_page=_default_load_page)

    url = random_url()
    receive_url_data(tester, url=url)

    _assert_have_run_loading_background_task(tester, _default_load_page, url)


def test_should_send_loaded_page_to_an_existing_waiter_first():
    existing_waiter = random_address()
    tester = create_empty_page_loader(waiters=[existing_waiter])

    loaded_page = random_page_data()
    page_loading_completed(tester, page=loaded_page)

    assert CapturedMessage(existing_waiter, loaded_page) in tester.capture.get_messages()


def test_should_send_loaded_page_to_next_waiter():
    tester = create_empty_page_loader(waiters=[random_address()])

    next_waiter = random_address()
    get_page(tester, sender=next_waiter)
    page_loading_completed(tester)  # for first waiter
    tester.capture.clear_messages()

    next_page_data = random_page_data()
    page_loading_completed(tester, page=next_page_data)  # for next waiter

    assert CapturedMessage(next_waiter, next_page_data) in tester.capture.get_messages()
