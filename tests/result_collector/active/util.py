from demo.core.result_collector import ResultData
from tests.util import random_string


def random_result_data() -> ResultData:
    return ResultData(content=random_string())
