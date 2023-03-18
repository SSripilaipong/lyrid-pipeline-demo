from dataclasses import dataclass

from lyrid import use_switch, switch, Address

from .base import UrlRepoBase
from ..core.url_repo import GetUrlAfter


@use_switch
@dataclass
class FullUrlRepo(UrlRepoBase):

    @switch.message(type=GetUrlAfter)
    def get_url_after_index(self, sender: Address, message: GetUrlAfter):
        self._send_url_to_requested_index(sender, message.subscription, message.index)
