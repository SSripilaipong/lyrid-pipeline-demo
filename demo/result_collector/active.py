from dataclasses import dataclass, field
from typing import Callable, List

from lyrid import use_switch, switch, Address

from demo.core.result_collector import ResultData
from demo.result_collector.base import ResultCollectorBase


@use_switch
@dataclass
class ActiveResultCollector(ResultCollectorBase):
    is_busy: bool = False
    buffer: List[ResultData] = field(default_factory=list)

    @switch.message(type=ResultData)
    def result_data(self, message: ResultData):
        self._ask_for_result()
        self.buffer.append(message)

    @switch.background_task_exited(exception=None)
    def saving_task_completed(self):
        self.is_busy = False

    @switch.after_receive()
    def after_receive(self):
        if len(self.buffer) >= self.buffer_size and not self.is_busy:
            self.is_busy = True
            self.run_in_background(self.save, args=(self.buffer,))
            self.buffer = []

    @classmethod
    def of(cls, self: ResultCollectorBase) -> 'ActiveResultCollector':
        return ActiveResultCollector.create(**self._base_params())

    @classmethod
    def create(cls, processors: List[Address], buffer_size: int,
               save: Callable[[List[ResultData]], None]) -> 'ActiveResultCollector':
        return ActiveResultCollector(buffer_size=buffer_size, processors=processors, save=save)
