from demo.page_loader import EmptyPageLoader, ActivePageLoader, FullPageLoader
from tests.page_loader.action import get_page, page_loading_completed
from tests.page_loader.idle.factory import create_idle_page_loader


def test_should_maintain_buffer_size_setting_between_states():
    tester = create_idle_page_loader(buffer_size=3)

    get_page(tester)  # len(waiters) == 1
    assert isinstance(tester.current_actor, EmptyPageLoader)

    page_loading_completed(tester)  # for existing waiter
    page_loading_completed(tester)  # len(pages) == 1
    assert isinstance(tester.current_actor, ActivePageLoader)

    page_loading_completed(tester)  # len(pages) == 2
    assert isinstance(tester.current_actor, ActivePageLoader)

    page_loading_completed(tester)  # len(pages) == 3
    assert isinstance(tester.current_actor, FullPageLoader)
