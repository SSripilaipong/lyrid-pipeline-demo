from lyrid import Address
from lyrid.testing import CapturedMessage

from demo.core.url_repo import UrlData
from tests.url_repo.action import get_url
from tests.url_repo.active.factory import create_active_url_repo


def test_should_allow_user_to_get_url():
    user = Address("$.someone")
    tester = create_active_url_repo(urls=["https://example.com/0"])

    get_url(tester, by=user)

    assert tester.capture.get_messages() == [CapturedMessage(user, UrlData("https://example.com/0"))]


def test_should_pass_next_url_for_the_next_user_if_asked():
    tester = create_active_url_repo(urls=["https://example.com/0", "https://example.com/1"])
    get_url(tester)
    tester.capture.clear_messages()

    next_user = Address("$.someone.1")
    get_url(tester, by=next_user)

    assert tester.capture.get_messages() == [CapturedMessage(next_user, UrlData("https://example.com/1"))]


def test_should_send_the_latest_url_when_the_same_user_requests_again():
    user = Address("$.someone.1")
    tester = create_active_url_repo(urls=["https://example.com/0", "https://example.com/1"])
    get_url(tester, by=user)
    tester.capture.clear_messages()

    get_url(tester, by=user)

    assert tester.capture.get_messages() == [CapturedMessage(user, UrlData("https://example.com/1"))]
