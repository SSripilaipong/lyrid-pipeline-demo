from dataclasses import dataclass, field
from typing import List, Dict

from lyrid import Actor, use_switch, Address

from demo.core.url_repo import UrlData


@use_switch
@dataclass
class UrlRepoBase(Actor):
    buffer_size: int
    latest_sent_indices: Dict[str, int] = field(default_factory=dict)
    latest_requested_indices: Dict[str, int] = field(default_factory=dict)
    global_index_to_send: int = 0
    urls: List[str] = field(default_factory=list)

    def _send_url_to_requested_index(self, address: Address, subscriber: str):
        self._send_url_at_index(address, subscriber, self.global_index_to_send)

    def _send_url_at_index(self, address: Address, subscriber: str, index_to_send):
        self.latest_sent_indices[subscriber] = index_to_send
        if index_to_send == self.global_index_to_send:
            self.global_index_to_send += 1

        self.tell(address, UrlData(index_to_send, self.urls[index_to_send]))
