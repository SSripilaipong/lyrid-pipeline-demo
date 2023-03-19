from lyrid import Address
from lyrid.testing import CapturedMessage

from demo.core.url_repo import UrlData
from tests.url_repo.action import get_url
from tests.url_repo.active.factory import create_active_url_repo


def test_should_allow_consumer_to_get_url():
    consumer = Address("$.someone")
    tester = create_active_url_repo(urls=["https://example.com/0"])

    get_url(tester, by=consumer)

    assert tester.capture.get_messages() == [CapturedMessage(consumer, UrlData("https://example.com/0"))]


def test_should_pass_next_url_for_the_next_consumer_if_asked():
    tester = create_active_url_repo(urls=["https://example.com/0", "https://example.com/1"])
    get_url(tester)
    tester.capture.clear_messages()

    next_consumer = Address("$.someone.1")
    get_url(tester, by=next_consumer)

    assert tester.capture.get_messages() == [CapturedMessage(next_consumer, UrlData("https://example.com/1"))]
