from demo.page_loader.active import ActivePageLoader
from demo.page_loader.empty import EmptyPageLoader
from tests.page_loader.action import page_loading_completed
from tests.page_loader.empty.factory import create_empty_page_loader
from tests.page_loader.util import random_page_data
from tests.util import random_address


def test_should_become_active_when_no_waiters_are_waiting_and_new_page_has_been_loaded():
    tester = create_empty_page_loader(waiters=[random_address()])

    page_loading_completed(tester, page=random_page_data())  # for existing waiter
    assert isinstance(tester.current_actor, EmptyPageLoader)

    page_loading_completed(tester, page=random_page_data())
    assert isinstance(tester.current_actor, ActivePageLoader)
