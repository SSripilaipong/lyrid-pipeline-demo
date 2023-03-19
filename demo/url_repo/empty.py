from collections import deque
from dataclasses import dataclass, field
from typing import List, Deque

from lyrid import use_switch, switch, Address

from demo.core.url_repo import AddUrls, GetUrl
from .base import UrlRepoBase


@use_switch
@dataclass
class EmptyUrlRepo(UrlRepoBase):
    waiters: Deque[Address] = field(default_factory=deque)

    @switch.message(type=GetUrl)
    def get_url(self, sender: Address):
        self.waiters.append(sender)

    @switch.message(type=AddUrls)
    def add_urls(self, message: AddUrls):
        self._add_urls(message.urls)

        if self.waiters:
            address = self.waiters.popleft()
            self._send_next_url_to_address(address)

    @switch.after_receive()
    def after_receive(self):
        if self._n_urls_left() >= self._buffer_size():
            from .full import FullUrlRepo
            self.become(FullUrlRepo.of(self))

        elif self._n_urls_left() > 0 and not self.waiters:
            from .active import ActiveUrlRepo
            self.become(ActiveUrlRepo.of(self))

    @classmethod
    def create(cls, buffer_size: int) -> UrlRepoBase:
        return EmptyUrlRepo(buffer_size)

    @classmethod
    def of(cls, self: UrlRepoBase, waiters: List[Address] | None = None) -> 'EmptyUrlRepo':
        return cls(**self._base_params(), waiters=deque(waiters or []))
