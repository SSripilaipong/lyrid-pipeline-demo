from demo.page_loader import EmptyPageLoader, ActivePageLoader
from tests.page_loader.action import get_page
from tests.page_loader.active.factory import create_active_page_loader
from tests.page_loader.util import random_page_data


def test_should_become_empty_when_no_pages_left_and_new_customer_request_for_a_page_data():
    tester = create_active_page_loader(pages=[random_page_data()])

    get_page(tester)  # get the last page
    assert isinstance(tester.current_actor, ActivePageLoader)

    get_page(tester)
    assert isinstance(tester.current_actor, EmptyPageLoader)
