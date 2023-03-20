from lyrid import Address
from lyrid.testing import ActorTester

from demo.core import common
from demo.core.page_loader import PageLoadedEvent, SubscribePage, GetPage
from tests.util import random_address, random_string


def start(tester: ActorTester):
    sender = random_address()

    tester.simulate.tell(common.Start(), by=sender)


def page_loaded(tester: ActorTester, *, content: str = None):
    content = content if content is not None else "<html>Hello</html>"

    tester.simulate.tell(PageLoadedEvent(content), by=tester.actor_address)


def subscribe_page(tester: ActorTester, *, sender: Address = None) -> str:
    sender = sender if sender is not None else random_address()
    subscription_key = random_string()

    tester.simulate.tell(SubscribePage(subscription_key), by=sender)

    return subscription_key


def get_page(tester: ActorTester, *, subscription_key: str = None, sender: Address = None):
    sender = sender if sender is not None else random_address()
    subscription_key = subscription_key if subscription_key is not None else random_string()

    tester.simulate.tell(GetPage(subscription_key), by=sender)
