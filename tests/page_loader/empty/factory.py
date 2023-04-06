from typing import Callable, List

from lyrid import Address
from lyrid.testing import ActorTester

from demo.core.page_loader import PageData
from demo.page_loader import EmptyPageLoader
from tests.util import random_address


def create_empty_page_loader(*, url_repo: Address | None = None,
                             load_page: Callable[[str], PageData] | None = None,
                             waiters: List[Address] | None = None) -> ActorTester:
    url_repo = url_repo if url_repo is not None else random_address()
    waiters = waiters if waiters is not None else [random_address()]

    if load_page is None:
        def load_page(_: str) -> PageData:
            return PageData("https://example.com/1234", "<html>abcdefg</html>")

    return ActorTester(EmptyPageLoader.create(url_repo, load_page, waiters=waiters))
