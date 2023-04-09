from dataclasses import dataclass, field
from typing import Callable, List

from lyrid import use_switch, switch, Address

from demo.core.result_collector import ResultData, GetResult
from demo.result_collector.base import ResultCollectorBase


@use_switch
@dataclass
class ActiveResultCollector(ResultCollectorBase):
    processor: Address
    save: Callable[[List[ResultData]], None]

    buffer: List[ResultData] = field(default_factory=list)

    @switch.message(type=ResultData)
    def result_data(self, message: ResultData):
        self.tell(self.processor, GetResult())
        self.buffer.append(message)

        if len(self.buffer) >= self.buffer_size:
            self.run_in_background(self.save, args=(self.buffer,))
            self.buffer = []

    @classmethod
    def of(cls, self: ResultCollectorBase, processor: Address,
           save: Callable[[List[ResultData]], None]) -> 'ActiveResultCollector':
        return ActiveResultCollector.create(buffer_size=self.buffer_size, processor=processor, save=save)

    @classmethod
    def create(cls, processor: Address, buffer_size: int,
               save: Callable[[List[ResultData]], None]) -> 'ActiveResultCollector':
        return ActiveResultCollector(buffer_size=buffer_size, processor=processor, save=save)
