from dataclasses import dataclass
from typing import Callable, List, Dict, Any

from lyrid import Actor, Address

from demo.core.result_collector import ResultData, GetResult


@dataclass
class ResultCollectorBase(Actor):
    buffer_size: int
    processors: List[Address]
    save: Callable[[List[ResultData]], None]

    def _ask_for_results_from_all_processors(self):
        for processor in self.processors:
            self.tell(processor, GetResult())

    def _base_params(self) -> Dict[str, Any]:
        return {key: self.__dict__[key] for key in ResultCollectorBase.__annotations__}
