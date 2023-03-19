from dataclasses import dataclass

from lyrid import use_switch, switch, Address

from .base import UrlRepoBase
from ..core.url_repo import GetUrl


@use_switch
@dataclass
class FullUrlRepo(UrlRepoBase):

    @switch.message(type=GetUrl)
    def get_url(self, sender: Address):
        self._send_next_url_to_address(sender)
