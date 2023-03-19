from dataclasses import dataclass
from typing import Dict, Any

from lyrid import Actor, Address


@dataclass
class PageLoaderBase(Actor):
    url_repo: Address

    def _base_params(self) -> Dict[str, Any]:
        return {key: self.__dict__[key] for key in self.__annotations__}
