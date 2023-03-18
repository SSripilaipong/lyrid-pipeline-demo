from lyrid import Address
from lyrid.testing import CapturedMessage

from demo.core.url_repo import UrlData
from tests.url_repo.action import add_url, get_url_after_index
from tests.url_repo.exhausted.factory import create_exhausted_url_repo


# noinspection DuplicatedCode
def test_should_send_url_to_waiting_subscriber_when_a_url_arrives():
    subscriber = Address("$.someone.1")
    tester = create_exhausted_url_repo()
    get_url_after_index(tester, -1, by=subscriber, auto_subscribe=True)
    tester.capture.clear_messages()

    add_url(tester, "https://example.com/0", ref_id="x", by=Address("$"))

    assert set(tester.capture.get_messages()) == {
        CapturedMessage(subscriber, UrlData(0, "https://example.com/0"))
    }


# noinspection DuplicatedCode
def test_should_send_url_to_multiple_waiting_subscriber_when_urls_arrive():
    subscriber1, subscriber2 = Address("$.someone.1"), Address("$.someone.2")
    tester = create_exhausted_url_repo()
    get_url_after_index(tester, -1, by=subscriber1, auto_subscribe=True)
    get_url_after_index(tester, -1, by=subscriber2, auto_subscribe=True)
    tester.capture.clear_messages()

    add_url(tester, "https://example.com/0", ref_id="x", by=Address("$"))
    add_url(tester, "https://example.com/1", ref_id="y", by=Address("$"))

    assert set(tester.capture.get_messages()) == {
        CapturedMessage(subscriber1, UrlData(0, "https://example.com/0")),
        CapturedMessage(subscriber2, UrlData(1, "https://example.com/1")),
    }
