from lyrid import Address
from lyrid.testing import CapturedMessage

from demo.core.url_repo import GetUrl
from tests.page_loader.action import get_page
from tests.page_loader.idle.factory import create_idle_page_loader


def test_should_get_page_from_url_repo():
    url_repo_addr = Address("$.tester.my_url_repo")
    tester = create_idle_page_loader(url_repo=url_repo_addr)

    get_page(tester)

    assert tester.capture.get_messages() == [CapturedMessage(url_repo_addr, GetUrl())]
