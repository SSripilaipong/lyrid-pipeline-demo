from collections import deque
from typing import List

from lyrid import Address
from lyrid.testing import ActorTester

from demo.core.page_loader import PageData
from demo.page_loader import FullPageLoader
from tests.page_loader.util import random_page_data
from tests.util import random_address


def create_full_page_loader(*, url_repo: Address | None = None, pages: List[PageData] | None = None) -> ActorTester:
    url_repo = url_repo if url_repo is not None else random_address()
    pages = pages if pages is not None else [random_page_data(), random_page_data()]

    def load_page(_: str) -> PageData:
        return random_page_data()

    return ActorTester(FullPageLoader.create(url_repo, len(pages), load_page, pages=deque(pages)))
