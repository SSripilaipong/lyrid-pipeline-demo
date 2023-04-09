from typing import Callable, List

from lyrid.testing import ActorTester

from demo.core.result_collector import ResultData
from demo.result_collector import ResultCollector


def create_result_collector(*, buffer_size: int = None, save: Callable[[List[ResultData]], None]) -> ActorTester:
    return ActorTester(ResultCollector(buffer_size=buffer_size, save=save))


def default_save(_: List[ResultData]) -> None: ...
