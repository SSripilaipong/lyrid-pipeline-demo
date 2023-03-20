from demo.page_loader import ActivePageLoader, EmptyPageLoader
from tests.page_loader.action import page_loaded, subscribe_page, get_page
from tests.page_loader.empty.factory import create_empty_page_loader


def test_should_become_active_when_page_loaded_event_occurred():
    tester = create_empty_page_loader()
    subscribe_page(tester)

    page_loaded(tester)

    assert isinstance(tester.current_actor, ActivePageLoader)


def test_should_not_become_active_if_there_is_a_waiter():
    tester = create_empty_page_loader()
    subscription = subscribe_page(tester)
    get_page(tester, subscription_key=subscription)
    get_page(tester, subscription_key=subscription)

    page_loaded(tester)

    assert isinstance(tester.current_actor, EmptyPageLoader)
