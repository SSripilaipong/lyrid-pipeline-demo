from collections import deque
from dataclasses import dataclass, field
from typing import Deque

from lyrid import Address, switch, use_switch

from demo.core.page_loader import PageLoadedEvent, GetPage
from demo.page_loader import ActivePageLoader
from demo.page_loader.base import PageLoaderBase


@dataclass
class Waiter:
    subscription_key: str
    requester: Address


@use_switch
@dataclass
class EmptyPageLoader(PageLoaderBase):
    waiters: Deque[Waiter] = field(default_factory=deque)

    @switch.message(type=PageLoadedEvent)
    def page_loaded(self):
        if len(self.waiters) == 0:
            self.become(ActivePageLoader.of(self))

    @switch.message(type=GetPage)
    def get_page(self, sender: Address, message: GetPage):
        self.waiters.append(Waiter(message.subscription_key, sender))

    @classmethod
    def of(cls, self: PageLoaderBase) -> PageLoaderBase:
        return EmptyPageLoader(**self._base_params())

    @classmethod
    def create(cls, url_repo: Address) -> 'PageLoaderBase':
        return EmptyPageLoader(url_repo)
