from typing import Callable

from lyrid import Address
from lyrid.testing import ActorTester

from demo.core.page_loader import PageData
from demo.page_loader.idle import IdlePageLoader
from tests.page_loader.util import random_page_data
from tests.util import random_address


def create_idle_page_loader(*, url_repo: Address | None = None, buffer_size: int | None = None,
                            load_page: Callable[[str], PageData] | None = None) -> ActorTester:
    url_repo = url_repo if url_repo is not None else random_address()
    buffer_size = buffer_size if buffer_size is not None else 999

    if load_page is None:
        def load_page(_: str) -> PageData: return random_page_data()

    return ActorTester(IdlePageLoader.create(url_repo, buffer_size, load_page))
