from dataclasses import dataclass, field
from typing import List, Dict

from lyrid import Actor, use_switch, switch, Address

from demo.core.url_repo import SubscribeUrlData, SubscribeUrlDataAck, UrlData


@use_switch
@dataclass
class UrlRepoBase(Actor):
    buffer_size: int
    latest_sent_indices: Dict[str, int] = field(default_factory=dict)
    latest_requested_indices: Dict[str, int] = field(default_factory=dict)
    global_index_to_send: int = 0
    urls: List[str] = field(default_factory=list)

    @switch.message(type=SubscribeUrlData)
    def subscribe(self, sender: Address, message: SubscribeUrlData):
        self.tell(sender, SubscribeUrlDataAck(message.subscription_key))

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
