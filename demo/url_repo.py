from dataclasses import dataclass

from lyrid import Actor, use_switch, switch, Address

from demo.core.url_repo import SubscribeUrlData, SubscribeUrlDataAck


@use_switch
@dataclass
class UrlRepo(Actor):
    @switch.message(type=SubscribeUrlData)
    def subscribe(self, sender: Address):
        self.tell(sender, SubscribeUrlDataAck())
