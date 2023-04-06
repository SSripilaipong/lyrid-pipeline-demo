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
        self._ask_for_url_from_repo()
        self.pages.append(result)

    @switch.message(type=GetPage)
    def get_page(self, sender: Address):
        if len(self.pages) > 0:
            page = self.pages.popleft()
            self.tell(sender, page)
        else:
            self.__become_empty(waiters=[sender])

    def __become_empty(self, waiters):
        from demo.page_loader import EmptyPageLoader
        self.become(EmptyPageLoader.of(self, waiters=waiters))

    @classmethod
    def of(cls, self: PageLoaderBase, *, pages: List[PageData]) -> 'ActivePageLoader':
        return ActivePageLoader.create(**self._base_params(), pages=pages)

    @classmethod
    def create(cls, url_repo: Address, load_page: Callable[[str], PageData], *,
               pages: List[PageData]) -> 'ActivePageLoader':
        return ActivePageLoader(url_repo, load_page, pages=deque(pages))
