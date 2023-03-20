from dataclasses import dataclass

from lyrid import Address, switch, use_switch

from demo.core.page_loader import PageLoadedEvent
from demo.page_loader import ActivePageLoader
from demo.page_loader.base import PageLoaderBase


@use_switch
@dataclass
class EmptyPageLoader(PageLoaderBase):

    @switch.message(type=PageLoadedEvent)
    def page_loaded(self):
        self.become(ActivePageLoader.of(self))

    @classmethod
    def of(cls, self: PageLoaderBase) -> PageLoaderBase:
        return EmptyPageLoader(**self._base_params())

    @classmethod
    def create(cls, url_repo: Address) -> 'PageLoaderBase':
        return EmptyPageLoader(url_repo)
