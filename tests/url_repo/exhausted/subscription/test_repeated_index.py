from demo.core.url_repo import UrlData
from tests.url_repo.action import get_url_after_index, add_url
from tests.url_repo.exhausted.factory import create_exhausted_url_repo


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
