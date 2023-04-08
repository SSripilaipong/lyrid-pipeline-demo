from lyrid.testing import CapturedMessage

from tests.page_loader.action import get_page, page_loading_completed
from tests.page_loader.active.factory import create_active_page_loader
from tests.page_loader.empty.factory import create_empty_page_loader
from tests.page_loader.util import random_page_data
from tests.util import random_address


def test_should_send_loaded_page_to_an_existing_waiter_asked_since_active_state_when_being_in_empty_state():
    tester = create_active_page_loader(pages=[random_page_data()])

    get_page(tester)  # get the last page
    get_page(tester, sender=(existing_waiter := random_address()))  # become empty

    page_loading_completed(tester, page=(loaded_page := random_page_data()))

    assert CapturedMessage(existing_waiter, loaded_page) in tester.capture.get_messages()


def test_should_buffer_loaded_page_from_empty_state_and_send_to_first_requesting_consumer_in_active_state():
    tester = create_empty_page_loader(waiters=[random_address()])

    page_loading_completed(tester)  # for existing waiter
    page_loading_completed(tester, page=(loaded_page := random_page_data()))  # for first consumer, become active
    tester.capture.clear_messages()

    get_page(tester, sender=(first_consumer := random_address()))

    assert CapturedMessage(first_consumer, loaded_page) in tester.capture.get_messages()
