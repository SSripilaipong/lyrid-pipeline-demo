from lyrid.testing import CapturedMessage

from tests.page_loader.action import get_page, page_loading_completed
from tests.page_loader.empty.factory import create_empty_page_loader
from tests.page_loader.idle.factory import create_idle_page_loader
from tests.page_loader.util import random_page_data
from tests.util import random_address


def test_should_send_loaded_page_to_an_existing_waiter_asked_since_idle_state():
    tester = create_idle_page_loader()

    get_page(tester, sender=(existing_waiter := random_address()))

    page_loading_completed(tester, page=(loaded_page := random_page_data()))

    assert CapturedMessage(existing_waiter, loaded_page) in tester.capture.get_messages()


def test_should_buffer_loaded_page_from_empty_state_and_send_to_first_requesting_consumer_in_active_state():
    tester = create_empty_page_loader(waiters=[random_address()])

    page_loading_completed(tester)  # for existing waiter
    page_loading_completed(tester, page=(loaded_page := random_page_data()))  # for first consumer, become active
    tester.capture.clear_messages()

    get_page(tester, sender=(first_consumer := random_address()))

    assert CapturedMessage(first_consumer, loaded_page) in tester.capture.get_messages()
