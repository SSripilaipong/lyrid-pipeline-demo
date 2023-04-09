from dataclasses import dataclass
from typing import Callable, Deque

from lyrid import use_switch, switch, Address

from demo.core.page_loader import PageData, GetPage
from demo.page_loader.base import PageLoaderBase


@use_switch
@dataclass
class FullPageLoader(PageLoaderBase):
    pages: Deque[PageData]

    @switch.message(type=GetPage)
    def get_page(self, sender: Address):
        page = self.pages.popleft()
        self.tell(sender, page)
        self._ask_for_url_from_repo()
        self.__become_active()

    def __become_active(self):
        from .active import ActivePageLoader
        self.become(ActivePageLoader.of(self, pages=self.pages))

    @classmethod
    def of(cls, self: PageLoaderBase, *, pages: Deque[PageData]) -> 'FullPageLoader':
        return FullPageLoader.create(**self._base_params(), pages=pages)

    @classmethod
    def create(cls, url_repo: Address, buffer_size: int, load_page: Callable[[str], PageData],
               pages: Deque[PageData]) -> 'FullPageLoader':
        return FullPageLoader(url_repo, buffer_size, load_page, pages)
