from lyrid import Address
from lyrid.testing import ActorTester

from demo.core import common
from tests.util import random_string


def start(tester: ActorTester):
    sender = Address(f"$.tester.{random_string()}")

    tester.simulate.tell(common.Start(), by=sender)
