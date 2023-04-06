from dataclasses import dataclass, field
from typing import Callable, List

from lyrid import use_switch, Address, switch

from demo.core.page_loader import PageData, GetPage
from demo.page_loader.base import PageLoaderBase


@use_switch
@dataclass
class ActivePageLoader(PageLoaderBase):
    pages: List[PageData] = field(default_factory=list)

    @switch.message(type=GetPage)
    def get_page(self, sender: Address):
        self.tell(sender, self.pages[0])

    @classmethod
    def of(cls, self: PageLoaderBase) -> 'ActivePageLoader':
        return ActivePageLoader(**self._base_params())

    @classmethod
    def create(cls, url_repo: Address, load_page: Callable[[str], PageData], *,
               pages: List[PageData]) -> 'PageLoaderBase':
        return ActivePageLoader(url_repo, load_page, pages=pages)
