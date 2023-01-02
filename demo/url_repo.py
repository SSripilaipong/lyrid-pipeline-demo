from dataclasses import dataclass, field
from typing import List, Dict

from lyrid import Actor, use_switch, switch, Address

from demo.core.url_repo import SubscribeUrlData, SubscribeUrlDataAck, AddUrl, AddUrlAck, GetUrlAfter, UrlData


@use_switch
@dataclass
class UrlRepo(Actor):
    subscription_indices: Dict[Address, int] = field(default_factory=dict)
    current_index: int = 0
    urls: List[str] = field(default_factory=list)

    @switch.message(type=AddUrl)
    def add_url(self, sender: Address, message: AddUrl):
        self.urls.append(message.url)
        self.tell(sender, AddUrlAck(message.ref_id))

    @switch.message(type=SubscribeUrlData)
    def subscribe(self, sender: Address):
        self.tell(sender, SubscribeUrlDataAck())

    @switch.message(type=GetUrlAfter)
    def get_url_after_index(self, sender: Address):
        index = self.subscription_indices.get(sender)
        if index is None:
            index = self.subscription_indices[sender] = self.current_index
            self.current_index += 1

        self.tell(sender, UrlData(index, self.urls[index]))
