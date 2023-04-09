from demo.page_loader.active import ActivePageLoader
from demo.page_loader.empty import EmptyPageLoader
from demo.page_loader.full import FullPageLoader
from tests.page_loader.action import get_page, page_loading_completed
from tests.page_loader.active.factory import create_active_page_loader
from tests.page_loader.util import random_page_data


def test_should_become_empty_when_no_pages_left_and_new_customer_request_for_a_page_data():
    tester = create_active_page_loader(pages=[random_page_data()])

    get_page(tester)  # get the last page
    assert isinstance(tester.current_actor, ActivePageLoader)

    get_page(tester)
    assert isinstance(tester.current_actor, EmptyPageLoader)


def test_should_become_full_when_buffer_is_full_after_page_loading_completed():
    tester = create_active_page_loader(pages=[random_page_data()], buffer_size=3)

    page_loading_completed(tester)
    assert isinstance(tester.current_actor, ActivePageLoader)

    page_loading_completed(tester)
    assert isinstance(tester.current_actor, FullPageLoader)
