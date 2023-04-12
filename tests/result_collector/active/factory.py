from typing import Callable, List

from lyrid import Address
from lyrid.testing import ActorTester

from demo.core.result_collector import ResultData
from demo.result_collector.active import ActiveResultCollector
from tests.util import random_address


def create_active_result_collector(*, buffer_size: int | None = None, processors: List[Address] | None = None,
                                   save: Callable[[List[ResultData]], None] | None = None) -> ActorTester:
    processors = processors if processors is not None else [random_address()]
    buffer_size = buffer_size if buffer_size is not None else 999
    if save is None:
        def save(_: List[ResultData]) -> None: ...

    return ActorTester(ActiveResultCollector.create(processors=processors, buffer_size=buffer_size, save=save))


def default_save(_: List[ResultData]) -> None: ...
