from lyrid import Address
from lyrid.testing import ActorTester, CapturedMessage

from demo.core.url_repo import SubscribeUrlData, SubscribeUrlDataAck
from demo.url_repo import UrlRepo


def test_should_tell_back_with_ack_message():
    subscriber = Address("$.someone")
    tester = ActorTester(UrlRepo())

    tester.simulate.tell(SubscribeUrlData("abc"), by=subscriber)

    assert tester.capture.get_messages() == [CapturedMessage(subscriber, SubscribeUrlDataAck("abc"))]
