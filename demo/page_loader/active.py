from collections import deque
from dataclasses import dataclass, field
from typing import Callable, List, Deque

from lyrid import use_switch, Address, switch

from demo.core.page_loader import PageData, GetPage
from demo.core.url_repo import UrlData
from demo.page_loader.base import PageLoaderBase


@use_switch
@dataclass
class ActivePageLoader(PageLoaderBase):
    buffer_size: int
    pages: Deque[PageData] = field(default_factory=deque)

    @switch.message(type=UrlData)
    def receive_url_data(self, message: UrlData):
        self._run_load_page_in_background(message.url)

    @switch.background_task_exited(exception=None)
    def page_loading_completed(self, result: PageData):
        self._ask_for_url_from_repo()
        self.pages.append(result)

        if len(self.pages) >= self.buffer_size:
            self.__become_full()

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

    def __become_full(self):
        from demo.page_loader import FullPageLoader
        self.become(FullPageLoader.of(self))

    @classmethod
    def of(cls, self: PageLoaderBase, *, pages: List[PageData]) -> 'ActivePageLoader':
        return ActivePageLoader.create(**self._base_params(), buffer_size=0, pages=pages)

    @classmethod
    def create(cls, url_repo: Address, load_page: Callable[[str], PageData], buffer_size: int, *,
               pages: List[PageData]) -> 'ActivePageLoader':
        return ActivePageLoader(url_repo, load_page, buffer_size, pages=deque(pages))
