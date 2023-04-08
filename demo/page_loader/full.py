from dataclasses import dataclass

from lyrid import use_switch

from demo.page_loader.base import PageLoaderBase


@use_switch
@dataclass
class FullPageLoader(PageLoaderBase):

    @classmethod
    def of(cls, self: PageLoaderBase) -> 'FullPageLoader':
        return FullPageLoader(**self._base_params())
