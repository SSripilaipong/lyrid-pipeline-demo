from dataclasses import dataclass
from typing import Dict, Any

from lyrid import Actor, Address

from demo.core.url_repo import GetUrl


@dataclass
class PageLoaderBase(Actor):
    url_repo: Address

    def _base_params(self) -> Dict[str, Any]:
        return {key: self.__dict__[key] for key in PageLoaderBase.__annotations__}

    def _get_url_from_repo(self):
        self.tell(self.url_repo, GetUrl())
