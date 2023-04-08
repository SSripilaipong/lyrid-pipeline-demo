from lyrid.testing import CapturedMessage

from tests.page_loader.action import page_loading_completed, get_page
from tests.page_loader.active.factory import create_active_page_loader
from tests.page_loader.util import random_page_data
from tests.util import random_address


def test_should_maintain_loaded_pages_between_active_state_and_full_state():
    tester = create_active_page_loader(pages=[first_page := random_page_data(), second_page := random_page_data()],
                                       buffer_size=3)

    page_loading_completed(tester)  # become full
    tester.capture.clear_messages()

    get_page(tester, sender=(first_consumer := random_address()))
    assert CapturedMessage(first_consumer, first_page) in tester.capture.get_messages()
    tester.capture.clear_messages()

    get_page(tester, sender=(second_consumer := random_address()))
    assert CapturedMessage(second_consumer, second_page) in tester.capture.get_messages()
