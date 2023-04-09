from collections import deque
from dataclasses import dataclass
from typing import Deque, Callable, List

from lyrid import Address, switch, use_switch

from demo.core.page_loader import GetPage, PageData
from demo.core.url_repo import UrlData
from demo.page_loader.base import PageLoaderBase


@use_switch
@dataclass
class EmptyPageLoader(PageLoaderBase):
    waiters: Deque[Address]

    @switch.message(type=UrlData)
    def receive_url_data(self, message: UrlData):
        self._run_load_page_in_background(message.url)

    @switch.background_task_exited(exception=None)
    def page_loading_completed(self, result: PageData):
        self._ask_for_url_from_repo()

        if len(self.waiters) > 0:
            waiter = self.waiters.popleft()
            self.tell(waiter, result)
        else:
            self.__become_active(pages=[result])

    @switch.message(type=GetPage)
    def get_page(self, sender: Address):
        self.waiters.append(sender)

    def __become_active(self, *, pages: List[PageData]):
        from .active import ActivePageLoader
        self.become(ActivePageLoader.of(self, pages=pages))

    @classmethod
    def of(cls, self: PageLoaderBase, *, waiters: List[Address]) -> 'EmptyPageLoader':
        return EmptyPageLoader.create(**self._base_params(), waiters=waiters)

    @classmethod
    def create(cls, url_repo: Address, buffer_size: int, load_page: Callable[[str], PageData],
               waiters: List[Address]) -> 'EmptyPageLoader':
        return EmptyPageLoader(url_repo, buffer_size, load_page, waiters=deque(waiters))
