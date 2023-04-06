from typing import List

from lyrid.testing import ActorTester

from demo.core.page_loader import PageData
from demo.page_loader import ActivePageLoader
from tests.page_loader.util import random_page_data
from tests.util import random_address


def create_active_page_loader(*, pages: List[PageData] | None = None) -> ActorTester:
    pages = pages if pages is not None else [random_page_data()]
    url_repo = random_address()

    def load_page(_: str) -> PageData:
        return random_page_data()

    return ActorTester(ActivePageLoader.create(url_repo, load_page, pages=pages))