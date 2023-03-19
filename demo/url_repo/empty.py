from collections import deque
from dataclasses import dataclass, field
from typing import List, Deque

from lyrid import use_switch, switch, Address

from demo.core.url_repo import AddUrl, GetUrl
from .base import UrlRepoBase


@use_switch
@dataclass
class EmptyUrlRepo(UrlRepoBase):
    waiters: Deque[Address] = field(default_factory=deque)

    @classmethod
    def of(cls, self: UrlRepoBase, waiters: List[Address] | None = None) -> 'EmptyUrlRepo':
        return cls(**self._base_params(), waiters=deque(waiters or []))

    @switch.message(type=GetUrl)
    def get_url(self, sender: Address):
        self.waiters.append(sender)

    @switch.message(type=AddUrl)
    def add_url(self, message: AddUrl):
        self.urls.append(message.url)

        if self.waiters:
            address = self.waiters.popleft()
            self._send_url_to_requested_index(address)

    @switch.after_receive()
    def after_receive(self):
        if self.index_to_send <= len(self.urls) - 1 and not self.waiters:
            from .active import ActiveUrlRepo
            self.become(ActiveUrlRepo.of(self))
