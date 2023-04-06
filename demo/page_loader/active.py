from dataclasses import dataclass

from lyrid import use_switch

from demo.page_loader.base import PageLoaderBase


@use_switch
@dataclass
class ActivePageLoader(PageLoaderBase):
    @classmethod
    def of(cls, self: PageLoaderBase) -> 'ActivePageLoader':
        return ActivePageLoader(**self._base_params())
