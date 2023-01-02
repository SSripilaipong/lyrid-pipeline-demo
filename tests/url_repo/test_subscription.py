from lyrid import Address
from lyrid.testing import ActorTester, CapturedMessage

from demo.core.url_repo import SubscribeUrlData, SubscribeUrlDataAck, AddUrl, GetUrlAfter, UrlData
from demo.url_repo import UrlRepo


def test_should_tell_back_with_ack_message():
    consumer = Address("$.someone")
    tester = ActorTester(UrlRepo())

    tester.simulate.tell(SubscribeUrlData(), by=consumer)

    assert tester.capture.get_messages() == [CapturedMessage(consumer, SubscribeUrlDataAck())]


def test_should_allow_subscriber_to_get_url_after_index():
    consumer = Address("$.someone")
    tester = ActorTester(UrlRepo())
    tester.simulate.tell(AddUrl("https://example.com/0", ref_id="x"), by=Address("$"))
    tester.simulate.tell(SubscribeUrlData(), by=consumer)
    tester.capture.clear_messages()

    tester.simulate.tell(GetUrlAfter(-1), by=consumer)

    assert tester.capture.get_messages() == [CapturedMessage(consumer, UrlData(0, "https://example.com/0"))]
