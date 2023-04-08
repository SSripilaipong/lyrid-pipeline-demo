from collections import deque
from dataclasses import dataclass
from typing import Callable, Deque, List

from lyrid import use_switch, switch, Address

from demo.core.page_loader import PageData, GetPage
from demo.page_loader.base import PageLoaderBase


@use_switch
@dataclass
class FullPageLoader(PageLoaderBase):
    pages: Deque[PageData]

    @switch.message(type=GetPage)
    def get_page(self, sender: Address):
        self.tell(sender, self.pages[0])
        self.__become_active(pages=[])

    def __become_active(self, *, pages: List[PageData]):
        from demo.page_loader import ActivePageLoader
        self.become(ActivePageLoader.of(self, pages=pages))

    @classmethod
    def of(cls, self: PageLoaderBase) -> 'FullPageLoader':
        return FullPageLoader.create(**self._base_params(), pages=deque())

    @classmethod
    def create(cls, url_repo: Address, buffer_size: int, load_page: Callable[[str], PageData],
               pages: Deque[PageData]) -> 'FullPageLoader':
        return FullPageLoader(url_repo, buffer_size, load_page, pages)
