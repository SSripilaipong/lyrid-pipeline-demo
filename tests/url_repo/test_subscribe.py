from lyrid import Address
from lyrid.testing import ActorTester, CapturedMessage

from demo.core.url_repo import SubscribeUrlData, SubscribeUrlDataAck
from demo.url_repo import UrlRepo


def test_should_tell_back_with_ack_message():
    repo = UrlRepo()
    tester = ActorTester(repo)

    consumer = Address("$.someone")
    tester.simulate.tell(SubscribeUrlData(), by=consumer)

    assert tester.capture.get_messages() == [CapturedMessage(consumer, SubscribeUrlDataAck())]
