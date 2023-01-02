from collections import deque
from dataclasses import dataclass, field
from typing import List, Dict, Deque, Tuple

from lyrid import Actor, use_switch, switch, Address

from demo.core.url_repo import SubscribeUrlData, SubscribeUrlDataAck, AddUrl, AddUrlAck, GetUrlAfter, UrlData


@use_switch
@dataclass
class UrlRepoBase(Actor):
    latest_sent_indices: Dict[str, int] = field(default_factory=dict)
    latest_requested_indices: Dict[str, int] = field(default_factory=dict)
    global_index_to_send: int = 0
    urls: List[str] = field(default_factory=list)

    def _handle_if_request_is_repeated(self, address: Address, subscriber: str, requested_index: int) -> bool:
        if requested_index < self.latest_requested_indices.get(subscriber, -1):  # ignore old request
            return True
        self.latest_requested_indices[subscriber] = requested_index

        latest_sent_index = self.latest_sent_indices.get(subscriber, -1)
        if requested_index < latest_sent_index:
            self._send_url_at_index(address, subscriber, latest_sent_index)
            return True

        return False

    def _send_url_to_requested_index(self, address: Address, subscriber: str, requested_index: int):
        if self._handle_if_request_is_repeated(address, subscriber, requested_index):
            return

        self._send_url_at_index(address, subscriber, self.global_index_to_send)

    def _send_url_at_index(self, address: Address, subscriber: str, index_to_send):
        self.latest_sent_indices[subscriber] = index_to_send
        if index_to_send == self.global_index_to_send:
            self.global_index_to_send += 1

        self.tell(address, UrlData(index_to_send, self.urls[index_to_send]))


@use_switch
@dataclass
class UrlRepo(UrlRepoBase):

    @classmethod
    def of(cls, self: UrlRepoBase) -> 'UrlRepo':
        return cls(
            self.latest_sent_indices, self.latest_requested_indices, self.global_index_to_send, self.urls,
        )

    @switch.message(type=AddUrl)
    def add_url(self, sender: Address, message: AddUrl):
        self.urls.append(message.url)
        self.tell(sender, AddUrlAck(message.ref_id))

    @switch.message(type=SubscribeUrlData)
    def subscribe(self, sender: Address, message: SubscribeUrlData):
        self.tell(sender, SubscribeUrlDataAck(message.subscription_key))

    @switch.message(type=GetUrlAfter)
    def get_url_after_index(self, sender: Address, message: GetUrlAfter):
        self._send_url_to_requested_index(sender, message.subscription, message.index)

    @switch.after_receive()
    def after_receive(self):
        if self.global_index_to_send > len(self.urls) - 1:
            self.become(EmptyUrlRepo.of(self))


@use_switch
@dataclass
class EmptyUrlRepo(UrlRepoBase):
    waiting_subscribers: Deque[Tuple[Address, str, int]] = field(default_factory=deque)

    @classmethod
    def of(cls, self: UrlRepoBase, waiting_subscribers: List[Tuple[Address, str, int]] | None = None) -> 'EmptyUrlRepo':
        return cls(
            self.latest_sent_indices, self.latest_requested_indices, self.global_index_to_send,
            self.urls, waiting_subscribers=deque(waiting_subscribers or []),
        )

    @switch.message(type=GetUrlAfter)
    def get_url_after_index(self, sender: Address, message: GetUrlAfter):
        if self._handle_if_request_is_repeated(sender, message.subscription, message.index):
            return

        self.waiting_subscribers.append((sender, message.subscription, message.index))

    @switch.message(type=AddUrl)
    def add_url(self, sender: Address, message: AddUrl):
        self.urls.append(message.url)
        self.tell(sender, AddUrlAck(message.ref_id))

        if self.waiting_subscribers:
            address, subscriber, requested_index = self.waiting_subscribers.popleft()
            self._send_url_to_requested_index(address, subscriber, requested_index)

    @switch.after_receive()
    def after_receive(self):
        if self.global_index_to_send <= len(self.urls) - 1 and not self.waiting_subscribers:
            self.become(UrlRepo.of(self))
