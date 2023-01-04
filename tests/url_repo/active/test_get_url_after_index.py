from lyrid import Address
from lyrid.testing import CapturedMessage

from demo.core.url_repo import UrlData
from demo.url_repo import ExhaustedUrlRepo
from tests.url_repo.action import get_url_after_index
from tests.url_repo.active.factory import create_active_url_repo_tester


# noinspection DuplicatedCode
def test_should_allow_subscriber_to_get_url_after_index():
    subscriber = Address("$.someone")
    tester = create_active_url_repo_tester(urls=["https://example.com/0"], subscribers=["xxx"])

    get_url_after_index(tester, -1, subscription="xxx", by=subscriber)

    assert tester.capture.get_messages() == [CapturedMessage(subscriber, UrlData(0, "https://example.com/0"))]


def test_should_pass_next_url_for_the_next_subscriber_if_asked():
    subscriber = Address("$.someone.1")
    tester = create_active_url_repo_tester(urls=["https://example.com/0", "https://example.com/1"], subscribers=["a"])
    get_url_after_index(tester, -1, auto_subscribe=True)
    tester.capture.clear_messages()

    get_url_after_index(tester, -1, subscription="a", by=subscriber)

    assert tester.capture.get_messages() == [CapturedMessage(subscriber, UrlData(1, "https://example.com/1"))]


# noinspection DuplicatedCode
def test_should_send_the_same_url_when_the_same_subscriber_requests_at_the_same_index():
    tester = create_active_url_repo_tester(urls=["https://example.com/0"], subscribers=["a"])
    tester.capture.clear_messages()

    get_url_after_index(tester, -1, subscription="a")
    first_messages = [cm.message for cm in tester.capture.get_messages()]
    tester.capture.clear_messages()

    get_url_after_index(tester, -1, subscription="a")
    second_messages = [cm.message for cm in tester.capture.get_messages()]

    assert first_messages == second_messages


# noinspection DuplicatedCode
def test_should_send_the_latest_url_when_the_same_subscriber_requests_at_later_index():
    subscriber = Address("$.someone.1")
    tester = create_active_url_repo_tester(urls=["https://example.com/0", "https://example.com/1"], subscribers=["a"])
    get_url_after_index(tester, -1, subscription="a", by=subscriber)
    tester.capture.clear_messages()

    get_url_after_index(tester, 0, subscription="a", by=subscriber)

    assert tester.capture.get_messages() == [CapturedMessage(subscriber, UrlData(1, "https://example.com/1"))]


# noinspection DuplicatedCode
def test_should_ignore_old_request_from_subscriber():
    subscriber = Address("$.someone.1")
    tester = create_active_url_repo_tester(urls=["https://example.com/0", "https://example.com/1"], subscribers=["a"])
    get_url_after_index(tester, -1, subscription="a", by=subscriber)
    get_url_after_index(tester, 0, subscription="a", by=subscriber)
    tester.capture.clear_messages()

    get_url_after_index(tester, -1, subscription="a", by=subscriber)

    assert tester.capture.get_messages() == []


# noinspection DuplicatedCode
def test_should_become_exhausted_when_all_urls_have_been_retrieved():
    tester = create_active_url_repo_tester(urls=["https://example.com/0", "https://example.com/1"], subscribers=["a"])

    get_url_after_index(tester, -1, subscription="a")
    get_url_after_index(tester, 0, subscription="a")

    assert isinstance(tester.current_actor, ExhaustedUrlRepo)
