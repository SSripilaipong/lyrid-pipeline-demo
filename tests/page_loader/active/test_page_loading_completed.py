from lyrid import Address
from lyrid.testing import CapturedMessage

from demo.core.page_loader import PageData
from tests.page_loader.action import subscribe_page, get_page, page_loading_completed
from tests.page_loader.active.factory import create_active_page_loader


def test_should_send_loaded_page_to_an_existing_waiter_first():
    tester = create_active_page_loader()

    subscriber = Address("$.tester.me")
    subscription = subscribe_page(tester, sender=subscriber)
    get_page(tester, subscription_key=subscription, sender=subscriber)

    page_loading_completed(tester, content="<html>Done!</html>")

    assert CapturedMessage(subscriber, PageData("<html>Done!</html>")) in tester.capture.get_messages()
