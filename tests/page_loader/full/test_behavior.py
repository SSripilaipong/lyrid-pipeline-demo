from lyrid.testing import CapturedMessage

from demo.core.url_repo import GetUrl
from tests.page_loader.action import get_page
from tests.page_loader.full.factory import create_full_page_loader
from tests.page_loader.util import random_page_data
from tests.util import random_address


def test_should_send_buffered_page_to_consumer_requesting_for_it():
    tester = create_full_page_loader(pages=[buffered_page := random_page_data(), random_address()])

    get_page(tester, sender=(consumer := random_address()))

    assert CapturedMessage(consumer, buffered_page) in tester.capture.get_messages()


def test_should_ask_for_url_from_repo_after_consumer_requested_a_page():
    tester = create_full_page_loader(url_repo=(url_repo := random_address()))

    get_page(tester)

    assert CapturedMessage(url_repo, GetUrl()) in tester.capture.get_messages()
