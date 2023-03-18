from dataclasses import dataclass

from lyrid import use_switch, switch, Address

from .base import UrlRepoBase
from ..core.url_repo import GetUrl


@use_switch
@dataclass
class FullUrlRepo(UrlRepoBase):

    @switch.message(type=GetUrl)
    def get_url_after_index(self, sender: Address, message: GetUrl):
        self._send_url_to_requested_index(sender, message.subscription)
