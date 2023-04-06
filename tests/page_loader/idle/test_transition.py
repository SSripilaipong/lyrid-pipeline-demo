from demo.page_loader import EmptyPageLoader
from tests.page_loader.action import get_page
from tests.page_loader.idle.factory import create_idle_page_loader


def test_should_become_empty_when_receiving_get_page_message():
    tester = create_idle_page_loader()

    get_page(tester)

    assert isinstance(tester.current_actor, EmptyPageLoader)
