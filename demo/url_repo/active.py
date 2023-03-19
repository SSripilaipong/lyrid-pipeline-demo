from dataclasses import dataclass
from typing import List

from lyrid import use_switch, switch, Address

from demo.core.url_repo import AddUrls, GetUrl
from .base import UrlRepoBase


@use_switch
@dataclass
class ActiveUrlRepo(UrlRepoBase):
    @switch.message(type=AddUrls)
    def add_urls(self, message: AddUrls):
        self._add_urls(message.urls)

    @switch.message(type=GetUrl)
    def get_url(self, sender: Address):
        self._send_next_url_to_address(sender)

    @switch.after_receive()
    def after_receive(self):
        if self._n_urls_left() == 0:
            from .empty import EmptyUrlRepo
            self.become(EmptyUrlRepo.of(self))

    @classmethod
    def create(cls, buffer_size: int, urls: List[str]) -> UrlRepoBase:
        return ActiveUrlRepo(buffer_size, urls=urls)

    @classmethod
    def of(cls, self: UrlRepoBase) -> 'ActiveUrlRepo':
        return cls(**self._base_params())
