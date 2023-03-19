from dataclasses import dataclass

from lyrid import use_switch, switch, Address

from demo.core.url_repo import AddUrl, GetUrl
from .base import UrlRepoBase


@use_switch
@dataclass
class ActiveUrlRepo(UrlRepoBase):

    @classmethod
    def of(cls, self: UrlRepoBase) -> 'ActiveUrlRepo':
        return cls(**self._base_params())

    @switch.message(type=AddUrl)
    def add_url(self, message: AddUrl):
        self.urls.append(message.url)

    @switch.message(type=GetUrl)
    def get_url(self, sender: Address):
        self._send_url_to_requested_index(sender)

    @switch.after_receive()
    def after_receive(self):
        if self.index_to_send > len(self.urls) - 1:
            from .empty import EmptyUrlRepo
            self.become(EmptyUrlRepo.of(self))
