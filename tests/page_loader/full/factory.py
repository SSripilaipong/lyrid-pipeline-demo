from collections import deque
from typing import List

from lyrid.testing import ActorTester

from demo.core.page_loader import PageData
from demo.page_loader import FullPageLoader
from tests.page_loader.util import random_page_data
from tests.util import random_address


def create_full_page_loader(*, pages: List[PageData] | None = None) -> ActorTester:
    pages = pages if pages is not None else [random_page_data()]

    def load_page(_: str) -> PageData:
        return random_page_data()

    return ActorTester(FullPageLoader.create(random_address(), len(pages), load_page, pages=deque(pages)))
