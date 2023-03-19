from demo.page_loader import EmptyWaitingForUrlPageLoader
from tests.page_loader.action import get_page
from tests.page_loader.idle.factory import create_idle_url_loader


def test_should_become_empty_waiting_for_url_when_receiving_get_page_message():
    tester = create_idle_url_loader()

    get_page(tester)

    assert isinstance(tester.current_actor, EmptyWaitingForUrlPageLoader)
