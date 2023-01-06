from dataclasses import dataclass

from lyrid import use_switch, switch, Address

from .base import UrlRepoBase
from ..core.url_repo import AddUrl, AddUrlAck


@use_switch
@dataclass
class FullUrlRepo(UrlRepoBase):

    @switch.message(type=AddUrl)
    def add_url(self, sender: Address, message: AddUrl):
        self.tell(sender, AddUrlAck(message.ref_id))
