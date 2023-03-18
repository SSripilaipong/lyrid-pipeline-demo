from lyrid import Address
from lyrid.testing import ActorTester, CapturedMessage

from demo.core.url_repo import SubscribeUrlData, SubscribeUrlDataAck


def assert_acknowledge_subscription(tester: ActorTester):
    subscriber = Address("$.someone")

    tester.simulate.tell(SubscribeUrlData("abc"), by=subscriber)

    assert tester.capture.get_messages() == [CapturedMessage(subscriber, SubscribeUrlDataAck("abc"))]
