from dataclasses import dataclass

from lyrid import use_switch, switch, Address

from demo.core import common
from demo.core.result_collector import GetResult
from demo.result_collector import ActiveResultCollector
from demo.result_collector.base import ResultCollectorBase


@use_switch
@dataclass
class IdleResultCollector(ResultCollectorBase):
    processor: Address

    @switch.message(type=common.Start)
    def start(self):
        self.tell(self.processor, GetResult())
        self.become(ActiveResultCollector.of(self, processor=Address("$"), save=None))

    @classmethod
    def create(cls, *, buffer_size: int, processor: Address) -> 'IdleResultCollector':
        return IdleResultCollector(buffer_size=buffer_size, processor=processor)
