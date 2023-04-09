from dataclasses import dataclass
from typing import Callable, List, Dict, Any

from lyrid import Actor, Address

from demo.core.result_collector import ResultData


@dataclass
class ResultCollectorBase(Actor):
    buffer_size: int
    processor: Address
    save: Callable[[List[ResultData]], None]

    def _base_params(self) -> Dict[str, Any]:
        return {key: self.__dict__[key] for key in ResultCollectorBase.__annotations__}
