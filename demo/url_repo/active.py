from dataclasses import dataclass

from lyrid import use_switch, switch, Address

from demo.core.url_repo import AddUrl, GetUrl
from .base import UrlRepoBase


@use_switch
@dataclass
class ActiveUrlRepo(UrlRepoBase):

    @classmethod
    def of(cls, self: UrlRepoBase) -> 'ActiveUrlRepo':
        return cls(
            self.buffer_size, self.latest_sent_indices, self.latest_requested_indices, self.global_index_to_send,
            self.urls,
        )

    @switch.message(type=AddUrl)
    def add_url(self, message: AddUrl):
        self.urls.append(message.url)

    @switch.message(type=GetUrl)
    def get_url(self, sender: Address, message: GetUrl):
        self._send_url_to_requested_index(sender, message.subscription)

    @switch.after_receive()
    def after_receive(self):
        if self.global_index_to_send > len(self.urls) - 1:
            from .exhausted import ExhaustedUrlRepo
            self.become(ExhaustedUrlRepo.of(self))
