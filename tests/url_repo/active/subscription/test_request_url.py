from lyrid import Address
from lyrid.testing import CapturedMessage

from demo.core.url_repo import UrlData
from tests.url_repo.action import get_url
from tests.url_repo.active.factory import create_active_url_repo


def test_should_allow_subscriber_to_get_url():
    subscriber = Address("$.someone")
    tester = create_active_url_repo(urls=["https://example.com/0"], subscribers=["xxx"])

    get_url(tester, subscription="xxx", by=subscriber)

    assert tester.capture.get_messages() == [CapturedMessage(subscriber, UrlData(0, "https://example.com/0"))]


def test_should_pass_next_url_for_the_next_subscriber_if_asked():
    subscriber = Address("$.someone.1")
    tester = create_active_url_repo(urls=["https://example.com/0", "https://example.com/1"], subscribers=["a"])
    get_url(tester, auto_subscribe=True)
    tester.capture.clear_messages()

    get_url(tester, subscription="a", by=subscriber)

    assert tester.capture.get_messages() == [CapturedMessage(subscriber, UrlData(1, "https://example.com/1"))]


def test_should_send_the_latest_url_when_the_same_subscriber_requests_again():
    subscriber = Address("$.someone.1")
    tester = create_active_url_repo(urls=["https://example.com/0", "https://example.com/1"], subscribers=["a"])
    get_url(tester, subscription="a", by=subscriber)
    tester.capture.clear_messages()

    get_url(tester, subscription="a", by=subscriber)

    assert tester.capture.get_messages() == [CapturedMessage(subscriber, UrlData(1, "https://example.com/1"))]
