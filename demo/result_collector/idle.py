from dataclasses import dataclass
from typing import Callable, List

from lyrid import use_switch, switch, Address

from demo.core import common
from demo.core.result_collector import GetResult, ResultData
from demo.result_collector import ActiveResultCollector
from demo.result_collector.base import ResultCollectorBase


@use_switch
@dataclass
class IdleResultCollector(ResultCollectorBase):

    @switch.message(type=common.Start)
    def start(self):
        self.tell(self.processor, GetResult())
        self.become(ActiveResultCollector.of(self))

    @classmethod
    def create(cls, *, buffer_size: int, processor: Address,
               save: Callable[[List[ResultData]], None]) -> 'IdleResultCollector':
        return IdleResultCollector(buffer_size=buffer_size, processor=processor, save=save)
