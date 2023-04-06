from demo.core.page_loader import PageData
from demo.page_loader import EmptyPageLoader, ActivePageLoader
from tests.page_loader.action import receive_url_data, page_loading_completed
from tests.page_loader.empty.factory import create_empty_page_loader
from tests.page_loader.util import random_page_data
from tests.util import random_address, random_url, random_html_content


def test_should_become_active_when_no_waiters_are_waiting_and_new_page_has_been_loaded():
    tester = create_empty_page_loader(waiters=[random_address()])

    page_loading_completed(tester, page=random_page_data())  # for existing waiter
    assert isinstance(tester.current_actor, EmptyPageLoader)

    page_loading_completed(tester, page=random_page_data())
    assert isinstance(tester.current_actor, ActivePageLoader)


def test_should_not_become_active_when_there_still_are_waiters():
    tester = create_empty_page_loader(waiters=[random_address(), random_address()])

    receive_url_data(tester, url=(url := random_url()))
    page_loading_completed(tester, page=PageData(url, random_html_content()))

    assert isinstance(tester.current_actor, EmptyPageLoader)
