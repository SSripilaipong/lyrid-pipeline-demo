from dataclasses import dataclass

from demo.page_loader.base import PageLoaderBase


@dataclass
class EmptyWaitingForUrlPageLoader(PageLoaderBase):

    @classmethod
    def of(cls, self: PageLoaderBase) -> PageLoaderBase:
        return EmptyWaitingForUrlPageLoader(**self._base_params())
