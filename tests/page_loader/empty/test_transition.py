from demo.core.page_loader import PageData
from demo.page_loader import ActivePageLoader, EmptyPageLoader
from tests.page_loader.action import receive_url_data, page_loading_completed
from tests.page_loader.empty.factory import create_empty_page_loader
from tests.util import random_address


def test_should_become_active_when_no_waiters_are_waiting():
    tester = create_empty_page_loader(waiters=[random_address()])

    receive_url_data(tester, url="https://example.com/123")
    assert isinstance(tester.current_actor, EmptyPageLoader)

    page_loading_completed(tester, page=PageData("https://example.com/123", "<html>OK!</html>"))
    assert isinstance(tester.current_actor, ActivePageLoader)


def test_should_not_become_active_when_there_still_are_waiters():
    tester = create_empty_page_loader(waiters=[random_address(), random_address()])

    receive_url_data(tester, url="https://example.com/123")
    page_loading_completed(tester, page=PageData("https://example.com/123", "<html>OK!</html>"))

    assert isinstance(tester.current_actor, EmptyPageLoader)
