from dataclasses import dataclass

from lyrid import use_switch, switch, Address

from demo.core import common
from demo.core.url_repo import GetUrl
from demo.page_loader import EmptyWaitingForUrlPageLoader
from demo.page_loader.base import PageLoaderBase


@use_switch
@dataclass
class IdlePageLoader(PageLoaderBase):

    @switch.message(type=common.Start)
    def start(self):
        self.tell(self.url_repo, GetUrl())

        self.become(EmptyWaitingForUrlPageLoader.of(self))

    @classmethod
    def create(cls, url_repo: Address) -> 'PageLoaderBase':
        return IdlePageLoader(url_repo)
