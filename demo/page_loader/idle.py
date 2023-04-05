from dataclasses import dataclass

from lyrid import use_switch, switch, Address

from demo.core import common
from demo.core.page_loader import PageData
from demo.page_loader import EmptyPageLoader
from demo.page_loader.base import PageLoaderBase


@use_switch
@dataclass
class IdlePageLoader(PageLoaderBase):

    @switch.message(type=common.Start)
    def start(self):
        self._ask_for_url_from_repo()
        self.become(EmptyPageLoader.of(self))

    @classmethod
    def create(cls, url_repo: Address) -> 'PageLoaderBase':
        return IdlePageLoader(url_repo, lambda _: PageData("", ""))
