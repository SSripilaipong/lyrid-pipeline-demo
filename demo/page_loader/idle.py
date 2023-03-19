from dataclasses import dataclass

from lyrid import use_switch, switch

from demo.core.page_loader import GetPage
from demo.page_loader import EmptyWaitingForUrlPageLoader
from demo.page_loader.base import PageLoaderBase


@use_switch
@dataclass
class IdlePageLoader(PageLoaderBase):

    @switch.message(type=GetPage)
    def get_page(self):
        self.become(EmptyWaitingForUrlPageLoader.create())

    @classmethod
    def create(cls) -> 'PageLoaderBase':
        return IdlePageLoader()
