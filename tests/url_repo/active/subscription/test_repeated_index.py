from lyrid import Address

from tests.url_repo.action import get_url_after_index
from tests.url_repo.active.factory import create_active_url_repo


# noinspection DuplicatedCode
def test_should_send_the_same_url_when_the_same_subscriber_requests_at_the_same_index():
    tester = create_active_url_repo(urls=["https://example.com/0"], subscribers=["a"])
    tester.capture.clear_messages()

    get_url_after_index(tester, -1, subscription="a")
    first_messages = [cm.message for cm in tester.capture.get_messages()]
    tester.capture.clear_messages()

    get_url_after_index(tester, -1, subscription="a")
    second_messages = [cm.message for cm in tester.capture.get_messages()]

    assert first_messages == second_messages


# noinspection DuplicatedCode
def test_should_ignore_old_request_from_subscriber():
    subscriber = Address("$.someone.1")
    tester = create_active_url_repo(urls=["https://example.com/0", "https://example.com/1"], subscribers=["a"])
    get_url_after_index(tester, -1, subscription="a", by=subscriber)
    get_url_after_index(tester, 0, subscription="a", by=subscriber)
    tester.capture.clear_messages()

    get_url_after_index(tester, -1, subscription="a", by=subscriber)

    assert tester.capture.get_messages() == []
