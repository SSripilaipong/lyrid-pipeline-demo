from lyrid import Address
from lyrid.testing import ActorTester, CapturedMessage

from demo.core.url_repo import SubscribeUrlData, SubscribeUrlDataAck, AddUrl, GetUrlAfter, UrlData
from demo.url_repo import UrlRepo


def test_should_tell_back_with_ack_message():
    subscriber = Address("$.someone")
    tester = ActorTester(UrlRepo())

    tester.simulate.tell(SubscribeUrlData(), by=subscriber)

    assert tester.capture.get_messages() == [CapturedMessage(subscriber, SubscribeUrlDataAck())]


def test_should_allow_subscriber_to_get_url_after_index():
    subscriber = Address("$.someone")
    tester = ActorTester(UrlRepo())
    tester.simulate.tell(AddUrl("https://example.com/0", ref_id="x"), by=Address("$"))
    tester.simulate.tell(SubscribeUrlData(), by=subscriber)
    tester.capture.clear_messages()

    tester.simulate.tell(GetUrlAfter(-1), by=subscriber)

    assert tester.capture.get_messages() == [CapturedMessage(subscriber, UrlData(0, "https://example.com/0"))]


def test_should_pass_next_url_for_the_next_subscriber_if_asked():
    subscriber1 = Address("$.someone.1")
    subscriber2 = Address("$.someone.2")
    tester = ActorTester(UrlRepo())
    tester.simulate.tell(AddUrl("https://example.com/0", ref_id="x"), by=Address("$"))
    tester.simulate.tell(AddUrl("https://example.com/1", ref_id="x"), by=Address("$"))
    tester.simulate.tell(SubscribeUrlData(), by=subscriber1)
    tester.simulate.tell(SubscribeUrlData(), by=subscriber2)
    tester.simulate.tell(GetUrlAfter(-1), by=subscriber1)
    tester.capture.clear_messages()

    tester.simulate.tell(GetUrlAfter(-1), by=subscriber2)

    assert tester.capture.get_messages() == [CapturedMessage(subscriber2, UrlData(1, "https://example.com/1"))]
