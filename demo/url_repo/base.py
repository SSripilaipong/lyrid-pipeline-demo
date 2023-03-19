from dataclasses import dataclass, field
from typing import List, Dict, Any

from lyrid import Actor, use_switch, Address, switch

from demo.core import common
from demo.core.url_repo import UrlData


@use_switch
@dataclass
class UrlRepoBase(Actor):
    buffer_size: int
    index_to_send: int = 0
    urls: List[str] = field(default_factory=list)

    @switch.ask(type=common.Stop)
    def ask_to_stop(self, sender: Address, ref_id: str):
        self.reply(sender, common.Ok(), ref_id=ref_id)

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
        space_left = self._buffer_size() - self._n_urls_left()
        n_urls_to_add = min(len(urls), space_left)

        self.urls.extend(urls[:n_urls_to_add])


def create_url_repo(buffer_size: int) -> UrlRepoBase:
    from .empty import EmptyUrlRepo
    return EmptyUrlRepo.create(buffer_size)
