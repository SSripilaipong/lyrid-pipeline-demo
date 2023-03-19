from lyrid import Address
from lyrid.testing import CapturedMessage

from demo.core.url_repo import UrlData
from tests.url_repo.action import add_urls, get_url
from tests.url_repo.empty.factory import create_empty_url_repo


def test_should_send_url_to_waiting_consumer_when_a_url_arrives():
    consumer = Address("$.someone.1")
    tester = create_empty_url_repo()
    get_url(tester, by=consumer)
    tester.capture.clear_messages()

    add_urls(tester, ["https://example.com/0"], by=Address("$"))

    assert tester.capture.get_messages() == [CapturedMessage(consumer, UrlData("https://example.com/0"))]


def test_should_send_url_to_multiple_waiting_consumers_when_urls_arrive_one_by_one():
    consumer1, consumer2 = Address("$.someone.1"), Address("$.someone.2")
    tester = create_empty_url_repo()
    get_url(tester, by=consumer1)
    get_url(tester, by=consumer2)
    tester.capture.clear_messages()

    add_urls(tester, ["https://example.com/0"], by=Address("$"))
    add_urls(tester, ["https://example.com/1"], by=Address("$"))

    assert set(tester.capture.get_messages()) == {
        CapturedMessage(consumer1, UrlData("https://example.com/0")),
        CapturedMessage(consumer2, UrlData("https://example.com/1")),
    }


def test_should_send_url_to_multiple_waiting_consumers_when_urls_arrive_all_at_once():
    consumer1, consumer2 = Address("$.someone.1"), Address("$.someone.2")
    tester = create_empty_url_repo()
    get_url(tester, by=consumer1)
    get_url(tester, by=consumer2)
    tester.capture.clear_messages()

    add_urls(tester, ["https://example.com/0", "https://example.com/1"], by=Address("$"))

    assert set(tester.capture.get_messages()) == {
        CapturedMessage(consumer1, UrlData("https://example.com/0")),
        CapturedMessage(consumer2, UrlData("https://example.com/1")),
    }
