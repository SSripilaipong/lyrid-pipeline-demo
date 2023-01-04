from lyrid import Address
from lyrid.testing import CapturedMessage

from demo.core.url_repo import UrlData, AddUrlAck
from demo.url_repo import ExhaustedUrlRepo, ActiveUrlRepo
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
        CapturedMessage(Address("$"), AddUrlAck(ref_id="x")),
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
        CapturedMessage(Address("$"), AddUrlAck(ref_id="x")),
        CapturedMessage(Address("$"), AddUrlAck(ref_id="y")),
        CapturedMessage(subscriber1, UrlData(0, "https://example.com/0")),
        CapturedMessage(subscriber2, UrlData(1, "https://example.com/1")),
    }


def test_should_become_active_when_no_waiting_actor_and_has_an_extra_url():
    tester = create_exhausted_url_repo()
    get_url_after_index(tester, -1, auto_subscribe=True)

    add_url(tester, "https://example.com/0")
    assert isinstance(tester.current_actor, ExhaustedUrlRepo)

    add_url(tester, "https://example.com/1")
    assert isinstance(tester.current_actor, ActiveUrlRepo)


# noinspection DuplicatedCode
def test_should_send_the_same_url_when_the_same_subscriber_requests_at_the_same_index():
    tester = create_exhausted_url_repo(subscribers=["a"])
    get_url_after_index(tester, -1, subscription="a")
    tester.capture.clear_messages()

    add_url(tester, "https://example.com/0")
    first_time_data_only = [cm.message for cm in tester.capture.get_messages() if isinstance(cm.message, UrlData)]
    tester.capture.clear_messages()

    get_url_after_index(tester, -1, subscription="a")
    second_time_data_only = [cm.message for cm in tester.capture.get_messages() if isinstance(cm.message, UrlData)]

    assert first_time_data_only == second_time_data_only


# noinspection DuplicatedCode
def test_should_ignore_old_request_from_subscriber():
    tester = create_exhausted_url_repo(subscribers=["a"])
    get_url_after_index(tester, -1, subscription="a")
    add_url(tester, "https://example.com/0")
    get_url_after_index(tester, 0, subscription="a")
    add_url(tester, "https://example.com/1")
    tester.capture.clear_messages()

    get_url_after_index(tester, -1, subscription="a")

    assert tester.capture.get_messages() == []
