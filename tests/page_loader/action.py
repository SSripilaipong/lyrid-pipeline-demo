from lyrid import Address
from lyrid.testing import ActorTester

from demo.core import common
from demo.core.page_loader import SubscribePage, GetPage
from demo.core.url_repo import UrlData
from tests.util import random_address, random_string


def start(tester: ActorTester):
    sender = random_address()

    tester.simulate.tell(common.Start(), by=sender)


def page_loading_completed(tester: ActorTester, *, content: str | None = None):
    content = content if content is not None else "<html>Hello</html>"

    tester.simulate.background_task_exit("xxx", return_value=content)


def subscribe_page(tester: ActorTester, *, sender: Address | None = None) -> str:
    sender = sender if sender is not None else random_address()
    subscription_key = random_string()

    tester.simulate.tell(SubscribePage(subscription_key), by=sender)

    return subscription_key


def get_page(tester: ActorTester, *, subscription_key: str | None = None, sender: Address | None = None):
    sender = sender if sender is not None else random_address()
    subscription_key = subscription_key if subscription_key is not None else random_string()

    tester.simulate.tell(GetPage(subscription_key), by=sender)


def receive_url_data(tester: ActorTester, *, url: str | None = None):
    sender = random_address()
    url = url if url is not None else "https://example.com/999"

    tester.simulate.tell(UrlData(url), by=sender)
