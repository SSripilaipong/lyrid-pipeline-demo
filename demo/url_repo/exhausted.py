from collections import deque
from dataclasses import dataclass, field
from typing import List, Deque, Tuple

from lyrid import use_switch, switch, Address

from demo.core.url_repo import AddUrl, GetUrlAfter
from .base import UrlRepoBase


@use_switch
@dataclass
class ExhaustedUrlRepo(UrlRepoBase):
    waiting_subscribers: Deque[Tuple[Address, str, int]] = field(default_factory=deque)

    @classmethod
    def of(cls, self: UrlRepoBase,
           waiting_subscribers: List[Tuple[Address, str, int]] | None = None) -> 'ExhaustedUrlRepo':
        return cls(
            self.buffer_size, self.latest_sent_indices, self.latest_requested_indices, self.global_index_to_send,
            self.urls, waiting_subscribers=deque(waiting_subscribers or []),
        )

    @switch.message(type=GetUrlAfter)
    def get_url_after_index(self, sender: Address, message: GetUrlAfter):
        if self._handle_if_request_is_repeated(sender, message.subscription, message.index):
            return

        self.waiting_subscribers.append((sender, message.subscription, message.index))

    @switch.message(type=AddUrl)
    def add_url(self, message: AddUrl):
        self.urls.append(message.url)

        if self.waiting_subscribers:
            address, subscriber, requested_index = self.waiting_subscribers.popleft()
            self._send_url_to_requested_index(address, subscriber, requested_index)

    @switch.after_receive()
    def after_receive(self):
        if self.global_index_to_send <= len(self.urls) - 1 and not self.waiting_subscribers:
            from .active import ActiveUrlRepo
            self.become(ActiveUrlRepo.of(self))
