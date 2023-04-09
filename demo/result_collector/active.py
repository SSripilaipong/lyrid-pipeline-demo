from dataclasses import dataclass, field
from typing import Callable, List

from lyrid import Actor, use_switch, switch, Address

from demo.core.result_collector import ResultData, GetResult


@use_switch
@dataclass
class ActiveResultCollector(Actor):
    processor: Address
    buffer_size: int
    save: Callable[[List[ResultData]], None]

    buffer: List[ResultData] = field(default_factory=list)

    @switch.message(type=ResultData)
    def result_data(self, message: ResultData):
        self.tell(self.processor, GetResult())
        self.buffer.append(message)

        if len(self.buffer) >= self.buffer_size:
            self.run_in_background(self.save, args=(self.buffer,))
            self.buffer = []
