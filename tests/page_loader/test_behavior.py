from lyrid import Address
from lyrid.testing import CapturedMessage

from demo.core.page_loader import PageData
from tests.page_loader.action import get_page, page_loading_completed
from tests.page_loader.idle.factory import create_idle_page_loader


def test_should_send_loaded_page_to_an_existing_waiter_asked_since_idle_state():
    tester = create_idle_page_loader()

    existing_waiter = Address("$.tester.me")
    get_page(tester, sender=existing_waiter)

    page_loading_completed(tester, page=PageData("https://example.com/1", "<html>Done!</html>"))

    assert CapturedMessage(
        existing_waiter, PageData("https://example.com/1", "<html>Done!</html>"),
    ) in tester.capture.get_messages()
