from lyrid import Address
from lyrid.testing import CapturedMessage

from demo.core.page_loader import PageData
from demo.core.url_repo import GetUrl
from tests.page_loader.action import subscribe_page, get_page, page_loaded, receive_url_data
from tests.page_loader.empty.factory import create_empty_page_loader


def test_should_send_loaded_page_to_an_existing_waiter_first():
    tester = create_empty_page_loader()

    subscriber = Address("$.tester.me")
    subscription = subscribe_page(tester, sender=subscriber)
    get_page(tester, subscription_key=subscription, sender=subscriber)

    page_loaded(tester, content="<html>Done!</html>")

    assert CapturedMessage(subscriber, PageData("<html>Done!</html>")) in tester.capture.get_messages()


def test_should_get_next_url_when_receiving_url_data():
    url_repo = Address("$.tester.r")
    tester = create_empty_page_loader(url_repo=url_repo)

    receive_url_data(tester)

    assert CapturedMessage(url_repo, GetUrl()) in tester.capture.get_messages()


def test_should_run_page_loading_background_task_when_receiving_url_data():
    url_repo = Address("$.tester.r")
    load_page = LoadPageMock()
    tester = create_empty_page_loader(url_repo=url_repo, load_page=load_page.function)

    receive_url_data(tester, url="https://example.com/123")

    tasks = tester.capture.get_background_tasks()
    assert len(tasks) == 1
    task_call = tasks[0]

    task_call.task(*task_call.args)
    assert load_page.url == "https://example.com/123"


class LoadPageMock:
    def __init__(self):
        self.url = None

    def function(self, url: str) -> str:
        self.url = url
        return ""
