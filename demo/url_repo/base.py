from dataclasses import dataclass, field
from typing import List

from lyrid import Actor, use_switch, Address

from demo.core.url_repo import UrlData


@use_switch
@dataclass
class UrlRepoBase(Actor):
    buffer_size: int
    index_to_send: int = 0
    urls: List[str] = field(default_factory=list)

    def _send_url_to_requested_index(self, address: Address):
        self.tell(address, UrlData(self.urls[self.index_to_send]))
        self.index_to_send += 1
