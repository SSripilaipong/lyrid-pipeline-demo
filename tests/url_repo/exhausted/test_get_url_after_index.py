from lyrid import Address
from lyrid.testing import CapturedMessage

from demo.core.url_repo import SubscribeUrlData, AddUrl, GetUrlAfter, UrlData, AddUrlAck
from tests.url_repo.exhausted.factory import create_exhausted_url_repo


# noinspection DuplicatedCode
def test_should_send_url_to_waiting_subscriber_when_a_url_arrives():
    subscriber = Address("$.someone.1")
    tester = create_exhausted_url_repo()
    tester.simulate.tell(SubscribeUrlData("a"), by=subscriber)
    tester.simulate.tell(GetUrlAfter("a", -1), by=subscriber)
    tester.capture.clear_messages()

    tester.simulate.tell(AddUrl("https://example.com/0", ref_id="x"), by=Address("$"))

    assert set(tester.capture.get_messages()) == {
        CapturedMessage(Address("$"), AddUrlAck(ref_id="x")),
        CapturedMessage(subscriber, UrlData(0, "https://example.com/0"))
    }


# noinspection DuplicatedCode
def test_should_send_url_to_multiple_waiting_subscriber_when_urls_arrive():
    subscriber1 = Address("$.someone.1")
    subscriber2 = Address("$.someone.2")
    tester = create_exhausted_url_repo()
    tester.simulate.tell(SubscribeUrlData("a"), by=subscriber1)
    tester.simulate.tell(SubscribeUrlData("b"), by=subscriber2)
    tester.simulate.tell(GetUrlAfter("a", -1), by=subscriber1)
    tester.simulate.tell(GetUrlAfter("b", -1), by=subscriber2)
    tester.capture.clear_messages()

    tester.simulate.tell(AddUrl("https://example.com/0", ref_id="x"), by=Address("$"))
    tester.simulate.tell(AddUrl("https://example.com/1", ref_id="y"), by=Address("$"))

    assert set(tester.capture.get_messages()) == {
        CapturedMessage(Address("$"), AddUrlAck(ref_id="x")),
        CapturedMessage(Address("$"), AddUrlAck(ref_id="y")),
        CapturedMessage(subscriber1, UrlData(0, "https://example.com/0")),
        CapturedMessage(subscriber2, UrlData(1, "https://example.com/1")),
    }
