from dataclasses import dataclass

from lyrid import Actor, use_switch, switch, Address

from demo.core import common
from demo.result_collector import ActiveResultCollector


@use_switch
@dataclass
class IdleResultCollector(Actor):
    @switch.message(type=common.Start)
    def start(self):
        self.become(ActiveResultCollector.create(processor=Address("$"), buffer_size=999, save=None))
