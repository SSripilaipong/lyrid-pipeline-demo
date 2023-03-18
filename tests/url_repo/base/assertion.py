from lyrid import Address
from lyrid.testing import ActorTester, CapturedMessage

from demo.core.url_repo import AddUrl, SubscribeUrlData, SubscribeUrlDataAck


def assert_not_acknowledge_add_url(tester: ActorTester):
    consumer = Address("$.someone")

    tester.simulate.tell(AddUrl("https://example.com/1", ref_id="ref123"), by=consumer)

    assert tester.capture.get_messages() == []


def assert_acknowledge_subscription(tester: ActorTester):
    subscriber = Address("$.someone")

    tester.simulate.tell(SubscribeUrlData("abc"), by=subscriber)

    assert tester.capture.get_messages() == [CapturedMessage(subscriber, SubscribeUrlDataAck("abc"))]
