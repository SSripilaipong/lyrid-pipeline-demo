from dataclasses import dataclass

from lyrid import Actor, use_switch, switch, Address

from demo.core import common
from demo.core.result_collector import GetResult
from demo.result_collector import ActiveResultCollector


@use_switch
@dataclass
class IdleResultCollector(Actor):
    processor: Address

    @switch.message(type=common.Start)
    def start(self):
        self.tell(self.processor, GetResult())
        self.become(ActiveResultCollector.create(processor=Address("$"), buffer_size=999, save=None))

    @classmethod
    def create(cls, *, processor: Address) -> 'IdleResultCollector':
        return IdleResultCollector(processor=processor)
