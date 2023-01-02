from dataclasses import dataclass, field
from typing import List

from lyrid import Actor, use_switch, switch, Address

from demo.core.url_repo import SubscribeUrlData, SubscribeUrlDataAck, AddUrl, AddUrlAck, GetUrlAfter, UrlData


@use_switch
@dataclass
class UrlRepo(Actor):
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
        self.tell(sender, UrlData(self.current_index, self.urls[self.current_index]))
        self.current_index += 1
