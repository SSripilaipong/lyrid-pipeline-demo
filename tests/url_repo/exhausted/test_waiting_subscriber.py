from lyrid import Address
from lyrid.testing import CapturedMessage

from demo.core.url_repo import UrlData
from tests.url_repo.action import add_url, get_url
from tests.url_repo.exhausted.factory import create_exhausted_url_repo


def test_should_send_url_to_waiting_user_when_a_url_arrives():
    user = Address("$.someone.1")
    tester = create_exhausted_url_repo()
    get_url(tester, by=user)
    tester.capture.clear_messages()

    add_url(tester, "https://example.com/0", ref_id="x", by=Address("$"))

    assert tester.capture.get_messages() == [
        CapturedMessage(user, UrlData(0, "https://example.com/0")),
    ]


def test_should_send_url_to_multiple_waiting_user_when_urls_arrive():
    user1, user2 = Address("$.someone.1"), Address("$.someone.2")
    tester = create_exhausted_url_repo()
    get_url(tester, by=user1)
    get_url(tester, by=user2)
    tester.capture.clear_messages()

    add_url(tester, "https://example.com/0", ref_id="x", by=Address("$"))
    add_url(tester, "https://example.com/1", ref_id="y", by=Address("$"))

    assert set(tester.capture.get_messages()) == {
        CapturedMessage(user1, UrlData(0, "https://example.com/0")),
        CapturedMessage(user2, UrlData(1, "https://example.com/1")),
    }
