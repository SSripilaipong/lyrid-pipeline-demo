from typing import Callable, List

from lyrid import Address

from demo.core.result_collector import ResultData
from demo.result_collector.idle import IdleResultCollector


def create_result_collector(processors: List[Address], *, buffer_size: int,
                            save: Callable[[List[ResultData]], None]) -> IdleResultCollector:
    return IdleResultCollector.create(buffer_size=buffer_size, processors=processors, save=save)
