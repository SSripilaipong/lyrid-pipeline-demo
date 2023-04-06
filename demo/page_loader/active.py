from collections import deque
from dataclasses import dataclass, field
from typing import Callable, List, Deque

from lyrid import use_switch, Address, switch

from demo.core.page_loader import PageData, GetPage
from demo.page_loader.base import PageLoaderBase


@use_switch
@dataclass
class ActivePageLoader(PageLoaderBase):
    pages: Deque[PageData] = field(default_factory=deque)

    @switch.background_task_exited(exception=None)
    def page_loading_completed(self, result: PageData):
        self.pages.append(result)

    @switch.message(type=GetPage)
    def get_page(self, sender: Address):
        page = self.pages.popleft()
        self.tell(sender, page)

    @classmethod
    def of(cls, self: PageLoaderBase) -> 'ActivePageLoader':
        return ActivePageLoader(**self._base_params())

    @classmethod
    def create(cls, url_repo: Address, load_page: Callable[[str], PageData], *,
               pages: List[PageData]) -> 'PageLoaderBase':
        return ActivePageLoader(url_repo, load_page, pages=deque(pages))
