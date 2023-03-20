from lyrid import Address

from demo.core.page_loader import PageLoadedEvent
from demo.page_loader import ActivePageLoader
from tests.page_loader.empty.factory import create_empty_page_loader


def test_should_become_active_when_background_task_completed():
    tester = create_empty_page_loader()

    tester.simulate.tell(PageLoadedEvent("<html>Hello</html>"), by=Address("$.tester.a"))

    assert isinstance(tester.current_actor, ActivePageLoader)
