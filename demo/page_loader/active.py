from collections import deque
from dataclasses import dataclass, field
from typing import Deque, Callable

from lyrid import Address, switch, use_switch

from demo.core.page_loader import GetPage, PageData
from demo.core.url_repo import UrlData
from demo.page_loader.base import PageLoaderBase


@dataclass
class Waiter:
    subscription_key: str
    address: Address


@use_switch
@dataclass
class ActivePageLoader(PageLoaderBase):
    url_buffer: Deque[str] = field(default_factory=deque)
    waiters: Deque[Waiter] = field(default_factory=deque)
    is_loading: bool = False

    @switch.message(type=UrlData)
    def receive_url_data(self, message: UrlData):
        self._get_url_from_repo()
        if not self.is_loading:
            self._run_load_page_in_background(message.url)
            self.is_loading = True
        else:
            self.url_buffer.append(message.url)

    @switch.background_task_exited(exception=None)
    def page_loading_completed(self, result: PageData):
        if len(self.url_buffer) == 0:
            self.is_loading = False
        else:
            url = self.url_buffer.popleft()
            self._run_load_page_in_background(url)

        if len(self.waiters) > 0:
            waiter = self.waiters.popleft()
            self.tell(waiter.address, result)

    @switch.message(type=GetPage)
    def get_page(self, sender: Address, message: GetPage):
        self.waiters.append(Waiter(message.subscription_key, sender))

    @classmethod
    def of(cls, self: PageLoaderBase) -> PageLoaderBase:
        return ActivePageLoader(**self._base_params())

    @classmethod
    def create(cls, url_repo: Address, load_page: Callable[[str], PageData]) -> 'PageLoaderBase':
        return ActivePageLoader(url_repo, load_page)
