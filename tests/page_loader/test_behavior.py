from lyrid.testing import CapturedMessage

from tests.page_loader.action import get_page, page_loading_completed
from tests.page_loader.idle.factory import create_idle_page_loader
from tests.page_loader.util import random_page_data
from tests.util import random_address


def test_should_send_loaded_page_to_an_existing_waiter_asked_since_idle_state():
    tester = create_idle_page_loader()

    existing_waiter = random_address()
    get_page(tester, sender=existing_waiter)

    loaded_page = random_page_data()
    page_loading_completed(tester, page=loaded_page)

    assert CapturedMessage(existing_waiter, loaded_page) in tester.capture.get_messages()
