from demo.page_loader import EmptyWaitingForUrlPageLoader
from tests.page_loader.action import start
from tests.page_loader.idle.factory import create_idle_page_loader


def test_should_become_empty_waiting_for_url_when_receiving_start_message():
    tester = create_idle_page_loader()

    start(tester)

    assert isinstance(tester.current_actor, EmptyWaitingForUrlPageLoader)
