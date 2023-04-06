from lyrid.testing import CapturedMessage

from demo.core.url_repo import GetUrl
from tests.page_loader.action import get_page, page_loading_completed
from tests.page_loader.active.factory import create_active_page_loader
from tests.page_loader.util import random_page_data
from tests.util import random_address


def test_should_buffer_loaded_page_until_a_consumer_requests_for_it():
    tester = create_active_page_loader(pages=[loaded_page := random_page_data()])

    get_page(tester, sender=(consumer := random_address()))

    assert CapturedMessage(consumer, loaded_page) in tester.capture.get_messages()


def test_should_buffer_next_loaded_page_for_the_next_consumer_requesting_for_it():
    tester = create_active_page_loader(pages=[random_page_data()])  # for first consumer
    page_loading_completed(tester, page=(next_loaded_page := random_page_data()))  # for next consumer

    get_page(tester)  # first consumer requests
    tester.capture.clear_messages()

    get_page(tester, sender=(next_consumer := random_address()))  # next consumer requests

    assert CapturedMessage(next_consumer, next_loaded_page) in tester.capture.get_messages()


def test_should_ask_for_url_from_repo_after_page_loading_task_is_completed():
    tester = create_active_page_loader(url_repo=(url_repo := random_address()))

    page_loading_completed(tester)

    assert CapturedMessage(url_repo, GetUrl()) in tester.capture.get_messages()
