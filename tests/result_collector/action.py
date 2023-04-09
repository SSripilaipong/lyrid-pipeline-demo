from lyrid.testing import ActorTester

from demo.core.result_collector import ResultData
from tests.util import random_address


def receive_result_data(tester: ActorTester, *, result_data: ResultData):
    tester.simulate.tell(result_data, by=random_address())
