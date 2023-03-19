from lyrid import Address
from lyrid.testing import ActorTester

from demo.core.page_loader import GetPage
from tests.util import random_string


def get_page(tester: ActorTester):
    sender = Address(f"$.tester.{random_string()}")

    tester.simulate.tell(GetPage(), by=sender)
