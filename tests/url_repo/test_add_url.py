from lyrid import Address
from lyrid.testing import ActorTester, CapturedMessage

from demo.core.url_repo import AddUrl, AddUrlAck
from demo.url_repo import UrlRepo


def test_should_allow_actor_to_add_url():
    consumer = Address("$.someone")
    tester = ActorTester(UrlRepo())

    tester.simulate.tell(AddUrl("https://example.com/1", ref_id="ref123"), by=consumer)

    assert tester.capture.get_messages() == [CapturedMessage(consumer, AddUrlAck(ref_id="ref123"))]
