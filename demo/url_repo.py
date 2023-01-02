from dataclasses import dataclass, field
from typing import List, Dict

from lyrid import Actor, use_switch, switch, Address

from demo.core.url_repo import SubscribeUrlData, SubscribeUrlDataAck, AddUrl, AddUrlAck, GetUrlAfter, UrlData


@use_switch
@dataclass
class UrlRepo(Actor):
    subscription_indices: Dict[str, int] = field(default_factory=dict)
    subscription_latest_requested_indices: Dict[str, int] = field(default_factory=dict)
    current_index: int = 0
    urls: List[str] = field(default_factory=list)

    @switch.message(type=AddUrl)
    def add_url(self, sender: Address, message: AddUrl):
        self.urls.append(message.url)
        self.tell(sender, AddUrlAck(message.ref_id))

    @switch.message(type=SubscribeUrlData)
    def subscribe(self, sender: Address, message: SubscribeUrlData):
        self.tell(sender, SubscribeUrlDataAck(message.subscription_key))

    @switch.message(type=GetUrlAfter)
    def get_url_after_index(self, sender: Address, message: GetUrlAfter):
        if message.index < self.subscription_latest_requested_indices.get(message.subscription, -1):
            return

        index = self.subscription_indices.get(message.subscription, -1)
        if index <= message.index:
            index = self.current_index

        self.subscription_indices[message.subscription] = index
        if index == self.current_index:
            self.current_index += 1
        self.subscription_latest_requested_indices[message.subscription] = message.index

        self.tell(sender, UrlData(index, self.urls[index]))
