from collections import deque
from dataclasses import dataclass, field
from typing import Deque, Callable, List

from lyrid import Address, switch, use_switch

from demo.core.page_loader import GetPage, PageData
from demo.core.url_repo import UrlData
from demo.page_loader import ActivePageLoader
from demo.page_loader.base import PageLoaderBase


@use_switch
@dataclass
class EmptyPageLoader(PageLoaderBase):
    waiters: Deque[Address] = field(default_factory=deque)

    @switch.message(type=UrlData)
    def receive_url_data(self, message: UrlData):
        self._run_load_page_in_background(message.url)

    @switch.background_task_exited(exception=None)
    def page_loading_completed(self, result: PageData):
        if len(self.waiters) == 0:
            self.become(ActivePageLoader.of(self))
            return

        waiter = self.waiters.popleft()
        self.tell(waiter, result)

    @switch.message(type=GetPage)
    def get_page(self, sender: Address):
        self.waiters.append(sender)

    @classmethod
    def of(cls, self: PageLoaderBase, *, waiters: List[Address]) -> PageLoaderBase:
        return EmptyPageLoader.create(**self._base_params(), waiters=waiters)

    @classmethod
    def create(cls, url_repo: Address, load_page: Callable[[str], PageData],
               waiters: List[Address]) -> 'PageLoaderBase':
        return EmptyPageLoader(url_repo, load_page, waiters=deque(waiters))
