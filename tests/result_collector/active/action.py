from lyrid import Address
from lyrid.testing import ActorTester

from demo.core.result_collector import ResultData
from tests.result_collector.active.util import random_result_data
from tests.util import random_address, random_string


def receive_result_data(tester: ActorTester, *, result_data: ResultData | None = None, by: Address | None = None):
    result_data = result_data if result_data is not None else random_result_data()
    by = by if by is not None else random_address()
    tester.simulate.tell(result_data, by=by)


def saving_completed(tester: ActorTester):
    tester.simulate.background_task_exit(random_string())
