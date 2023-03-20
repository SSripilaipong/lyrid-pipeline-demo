from dataclasses import dataclass

from lyrid import Address

from demo.page_loader.base import PageLoaderBase


@dataclass
class ActivePageLoader(PageLoaderBase):

    @classmethod
    def of(cls, self: PageLoaderBase) -> PageLoaderBase:
        return ActivePageLoader(**self._base_params())

    @classmethod
    def create(cls, url_repo: Address) -> 'PageLoaderBase':
        return ActivePageLoader(url_repo)
