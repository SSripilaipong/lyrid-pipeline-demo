from lyrid import Address
from lyrid.testing import CapturedMessage

from demo.core.url_repo import UrlData
from tests.url_repo.action import get_url
from tests.url_repo.full.factory import create_full_url_repo


def test_should_allow_user_to_get_url():
    user = Address("$.someone")
    tester = create_full_url_repo(urls=["https://example.com/0"])

    get_url(tester, by=user)

    assert tester.capture.get_messages() == [CapturedMessage(user, UrlData("https://example.com/0"))]
