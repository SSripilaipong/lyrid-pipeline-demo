from demo.page_loader.active import ActivePageLoader
from tests.page_loader.action import get_page
from tests.page_loader.full.factory import create_full_page_loader
from tests.page_loader.util import random_page_data


def test_should_become_active_after_a_consumer_gets_a_page():
    tester = create_full_page_loader(pages=[random_page_data(), random_page_data()])

    get_page(tester)

    assert isinstance(tester.current_actor, ActivePageLoader)
