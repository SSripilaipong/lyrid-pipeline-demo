from dataclasses import dataclass
from typing import List, Callable

from lyrid import use_switch, switch, Address

from demo.core.page_loader import PageData, GetPage
from demo.page_loader.base import PageLoaderBase


@use_switch
@dataclass
class IdlePageLoader(PageLoaderBase):

    @switch.message(type=GetPage)
    def get_page(self, sender: Address):
        self._ask_for_url_from_repo()
        self.__become_empty(waiters=[sender])

    def __become_empty(self, waiters: List[Address]):
        from .empty import EmptyPageLoader
        self.become(EmptyPageLoader.of(self, waiters=waiters))

    @classmethod
    def create(cls, url_repo: Address, buffer_size: int, load_page: Callable[[str], PageData]) -> 'IdlePageLoader':
        return IdlePageLoader(url_repo, buffer_size, load_page)
