from dataclasses import dataclass
from typing import List

from lyrid import use_switch, switch, Address

from .base import UrlRepoBase
from ..core.url_repo import GetUrl


@use_switch
@dataclass
class FullUrlRepo(UrlRepoBase):

    @switch.message(type=GetUrl)
    def get_url(self, sender: Address):
        self._send_next_url_to_address(sender)

    @classmethod
    def create(cls, urls: List[str]) -> UrlRepoBase:
        return FullUrlRepo(len(urls), urls=urls)

    @classmethod
    def of(cls, self: UrlRepoBase) -> UrlRepoBase:
        return FullUrlRepo(**self._base_params())
