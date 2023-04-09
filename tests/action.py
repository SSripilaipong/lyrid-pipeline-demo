from lyrid.testing import ActorTester

from demo.core import common
from tests.util import random_address


def start(tester: ActorTester):
    tester.simulate.tell(common.Start(), by=random_address())
