from dataclasses import dataclass, field
from typing import List, Dict, Any

from lyrid import Actor, use_switch, Address

from demo.core.url_repo import UrlData


@use_switch
@dataclass
class UrlRepoBase(Actor):
    buffer_size: int
    index_to_send: int = 0
    urls: List[str] = field(default_factory=list)

    def _send_next_url_to_address(self, address: Address):
        self.tell(address, UrlData(self.urls[self.index_to_send]))
        self.index_to_send += 1

    def _base_params(self) -> Dict[str, Any]:
        return {key: self.__dict__[key] for key in UrlRepoBase.__annotations__}

    def _n_urls_left(self) -> int:
        return len(self.urls) - self.index_to_send

    def _buffer_size(self) -> int:
        return self.buffer_size

    def _add_urls(self, urls: List[str]):
        self.urls.extend(urls)


def create_url_repo(buffer_size: int) -> UrlRepoBase:
    from .empty import EmptyUrlRepo
    return EmptyUrlRepo.create(buffer_size)
