from dataclasses import dataclass

from demo.page_loader.base import PageLoaderBase


@dataclass
class EmptyWaitingForUrlPageLoader(PageLoaderBase):

    @classmethod
    def create(cls) -> PageLoaderBase:
        return EmptyWaitingForUrlPageLoader()
