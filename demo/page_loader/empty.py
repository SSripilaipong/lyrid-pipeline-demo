from collections import deque
from dataclasses import dataclass, field
from typing import Deque, Callable

from lyrid import Address, switch, use_switch

from demo.core.page_loader import PageLoadedEvent, GetPage, PageData
from demo.core.url_repo import UrlData
from demo.page_loader import ActivePageLoader
from demo.page_loader.base import PageLoaderBase


@dataclass
class Waiter:
    subscription_key: str
    address: Address


@use_switch
@dataclass
class EmptyPageLoader(PageLoaderBase):
    waiters: Deque[Waiter] = field(default_factory=deque)

    @switch.message(type=UrlData)
    def receive_url_data(self, message: UrlData):
        self._get_url_from_repo()
        self._run_load_page_in_background(message.url)

    @switch.message(type=PageLoadedEvent)
    def page_loaded(self, message: PageLoadedEvent):
        if len(self.waiters) > 0:
            waiter = self.waiters.popleft()
            self.tell(waiter.address, PageData(message.content))

    @switch.message(type=GetPage)
    def get_page(self, sender: Address, message: GetPage):
        self.waiters.append(Waiter(message.subscription_key, sender))

    @switch.after_receive()
    def after_receive(self):
        if len(self.waiters) == 0:
            self.become(ActivePageLoader.of(self))

    @classmethod
    def of(cls, self: PageLoaderBase) -> PageLoaderBase:
        return EmptyPageLoader(**self._base_params())

    @classmethod
    def create(cls, url_repo: Address, load_page: Callable[[str], str]) -> 'PageLoaderBase':
        return EmptyPageLoader(url_repo, load_page)
