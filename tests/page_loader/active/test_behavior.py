from lyrid.testing import CapturedMessage

from tests.page_loader.action import get_page
from tests.page_loader.active.factory import create_active_page_loader
from tests.page_loader.util import random_page_data
from tests.util import random_address


def test_should_buffer_loaded_page_until_a_consumer_requests_for_it():
    loaded_page = random_page_data()
    tester = create_active_page_loader(pages=[loaded_page])

    consumer = random_address()
    get_page(tester, sender=consumer)

    assert tester.capture.get_messages() == [CapturedMessage(consumer, loaded_page)]
