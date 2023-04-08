from lyrid.testing import CapturedMessage

from tests.page_loader.action import get_page
from tests.page_loader.full.factory import create_full_page_loader
from tests.page_loader.util import random_page_data
from tests.util import random_address


def test_should_send_buffered_page_to_consumer_requesting_for_it():
    tester = create_full_page_loader(pages=[buffered_page := random_page_data(), random_address()])

    get_page(tester, sender=(consumer := random_address()))

    assert CapturedMessage(consumer, buffered_page) in tester.capture.get_messages()
