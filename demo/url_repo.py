from dataclasses import dataclass

from lyrid import Actor, use_switch, switch, Address

from demo.core.url_repo import SubscribeUrlData, SubscribeUrlDataAck, AddUrl, AddUrlAck


@use_switch
@dataclass
class UrlRepo(Actor):

    @switch.message(type=AddUrl)
    def add_url(self, sender: Address, message: AddUrl):
        self.tell(sender, AddUrlAck(message.ref_id))

    @switch.message(type=SubscribeUrlData)
    def subscribe(self, sender: Address):
        self.tell(sender, SubscribeUrlDataAck())
