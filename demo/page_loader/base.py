from dataclasses import dataclass
from typing import Dict, Any, Callable

from lyrid import Actor, Address

from demo.core.page_loader import PageData
from demo.core.url_repo import GetUrl


@dataclass
class PageLoaderBase(Actor):
    url_repo: Address
    load_page: Callable[[str], PageData]

    def _base_params(self) -> Dict[str, Any]:
        return {key: self.__dict__[key] for key in PageLoaderBase.__annotations__}

    def _ask_for_url_from_repo(self):
        self.tell(self.url_repo, GetUrl())

    def _run_load_page_in_background(self, url: str):
        self.run_in_background(self.load_page, args=(url,))
