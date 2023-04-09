from typing import Callable

from lyrid import Address

from demo.core.page_loader import PageData
from demo.page_loader.idle import IdlePageLoader


def create_page_loader(url_repo: Address, buffer_size: int, load_page: Callable[[str], PageData]) -> IdlePageLoader:
    return IdlePageLoader.create(url_repo=url_repo, buffer_size=buffer_size, load_page=load_page)
