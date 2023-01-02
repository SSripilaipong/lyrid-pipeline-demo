from lyrid import Address
from lyrid.testing import ActorTester, CapturedMessage

from demo.core.url_repo import SubscribeUrlData, AddUrl, GetUrlAfter, UrlData
from demo.url_repo import UrlRepo


# noinspection DuplicatedCode
def test_should_allow_subscriber_to_get_url_after_index():
    subscriber = Address("$.someone")
    tester = ActorTester(UrlRepo())
    tester.simulate.tell(AddUrl("https://example.com/0", ref_id="x"), by=Address("$"))
    tester.simulate.tell(SubscribeUrlData("xxx"), by=subscriber)
    tester.capture.clear_messages()

    tester.simulate.tell(GetUrlAfter("xxx", -1), by=subscriber)

    assert tester.capture.get_messages() == [CapturedMessage(subscriber, UrlData(0, "https://example.com/0"))]


def test_should_pass_next_url_for_the_next_subscriber_if_asked():
    subscriber1 = Address("$.someone.1")
    subscriber2 = Address("$.someone.2")
    tester = ActorTester(UrlRepo())
    tester.simulate.tell(AddUrl("https://example.com/0", ref_id="x"), by=Address("$"))
    tester.simulate.tell(AddUrl("https://example.com/1", ref_id="y"), by=Address("$"))
    tester.simulate.tell(SubscribeUrlData("a"), by=subscriber1)
    tester.simulate.tell(SubscribeUrlData("b"), by=subscriber2)
    tester.simulate.tell(GetUrlAfter("a", -1), by=subscriber1)
    tester.capture.clear_messages()

    tester.simulate.tell(GetUrlAfter("b", -1), by=subscriber2)

    assert tester.capture.get_messages() == [CapturedMessage(subscriber2, UrlData(1, "https://example.com/1"))]


# noinspection DuplicatedCode
def test_should_send_the_same_url_when_the_same_subscriber_requests_at_the_same_index():
    subscriber1 = Address("$.someone.1")
    subscriber2 = Address("$.someone.2")
    tester = ActorTester(UrlRepo())
    tester.simulate.tell(AddUrl("https://example.com/0", ref_id="x"), by=Address("$"))
    tester.simulate.tell(SubscribeUrlData("a"), by=subscriber1)
    tester.capture.clear_messages()

    tester.simulate.tell(GetUrlAfter("a", -1), by=subscriber1)
    first_time = tester.capture.get_messages()
    tester.capture.clear_messages()

    tester.simulate.tell(GetUrlAfter("a", -1), by=subscriber2)
    second_time = tester.capture.get_messages()

    assert first_time[0].message == second_time[0].message


# noinspection DuplicatedCode
def test_should_send_the_latest_url_when_the_same_subscriber_requests_at_later_index():
    subscriber = Address("$.someone.1")
    tester = ActorTester(UrlRepo())
    tester.simulate.tell(AddUrl("https://example.com/0", ref_id="x"), by=Address("$"))
    tester.simulate.tell(AddUrl("https://example.com/1", ref_id="y"), by=Address("$"))
    tester.simulate.tell(SubscribeUrlData("a"), by=subscriber)
    tester.simulate.tell(GetUrlAfter("a", -1), by=subscriber)
    tester.capture.clear_messages()

    tester.simulate.tell(GetUrlAfter("a", 0), by=subscriber)

    assert tester.capture.get_messages() == [CapturedMessage(subscriber, UrlData(1, "https://example.com/1"))]


# noinspection DuplicatedCode
def test_should_ignore_old_request_from_subscriber():
    subscriber = Address("$.someone.1")
    tester = ActorTester(UrlRepo())
    tester.simulate.tell(AddUrl("https://example.com/0", ref_id="x"), by=Address("$"))
    tester.simulate.tell(AddUrl("https://example.com/1", ref_id="y"), by=Address("$"))
    tester.simulate.tell(AddUrl("https://example.com/2", ref_id="y"), by=Address("$"))
    tester.simulate.tell(SubscribeUrlData("a"), by=subscriber)
    tester.simulate.tell(GetUrlAfter("a", -1), by=subscriber)
    tester.simulate.tell(GetUrlAfter("a", 0), by=subscriber)
    tester.capture.clear_messages()

    tester.simulate.tell(GetUrlAfter("a", -1), by=subscriber)

    assert tester.capture.get_messages() == []
