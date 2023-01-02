from collections import deque
from dataclasses import dataclass, field
from typing import List, Dict, Deque, Tuple

from lyrid import Actor, use_switch, switch, Address

from demo.core.url_repo import SubscribeUrlData, SubscribeUrlDataAck, AddUrl, AddUrlAck, GetUrlAfter, UrlData


@use_switch
@dataclass
class UrlRepoBase(Actor):
    latest_returned_indices: Dict[str, int] = field(default_factory=dict)
    latest_requested_indices: Dict[str, int] = field(default_factory=dict)
    global_index_to_return: int = 0
    urls: List[str] = field(default_factory=list)


@use_switch
@dataclass
class UrlRepo(UrlRepoBase):

    @switch.message(type=AddUrl)
    def add_url(self, sender: Address, message: AddUrl):
        self.urls.append(message.url)
        self.tell(sender, AddUrlAck(message.ref_id))

    @switch.message(type=SubscribeUrlData)
    def subscribe(self, sender: Address, message: SubscribeUrlData):
        self.tell(sender, SubscribeUrlDataAck(message.subscription_key))

    @switch.message(type=GetUrlAfter)
    def get_url_after_index(self, sender: Address, message: GetUrlAfter):
        requested_index, subscriber = message.index, message.subscription

        if requested_index < self.latest_requested_indices.get(subscriber, -1):  # ignore old request
            return
        self.latest_requested_indices[subscriber] = requested_index

        latest_returned_index = self.latest_returned_indices.get(subscriber, -1)
        index_to_return = latest_returned_index if requested_index < latest_returned_index else self.global_index_to_return

        if index_to_return > len(self.urls) - 1:
            self.become(EmptyUrlRepo.of(self, waiting_subscribers=[(sender, subscriber)]))
            return

        self.latest_returned_indices[subscriber] = index_to_return
        if index_to_return == self.global_index_to_return:
            self.global_index_to_return += 1

        self.tell(sender, UrlData(index_to_return, self.urls[index_to_return]))


@use_switch
@dataclass
class EmptyUrlRepo(UrlRepoBase):
    waiting_subscribers: Deque[Tuple[Address, str]] = field(default_factory=deque)

    @classmethod
    def of(cls, self: UrlRepoBase, waiting_subscribers: List[Tuple[Address, str]]) -> 'EmptyUrlRepo':
        return cls(
            self.latest_returned_indices, self.latest_requested_indices, self.global_index_to_return,
            self.urls, waiting_subscribers=deque(waiting_subscribers),
        )

    @switch.message(type=AddUrl)
    def add_url(self, sender: Address, message: AddUrl):
        self.urls.append(message.url)
        index_to_return = len(self.urls) - 1
        address, subscriber = self.waiting_subscribers.popleft()

        self.tell(sender, AddUrlAck(message.ref_id))
        self.tell(address, UrlData(index_to_return, self.urls[index_to_return]))
