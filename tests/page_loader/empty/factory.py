from typing import Callable

from lyrid import Address
from lyrid.testing import ActorTester

from demo.core.page_loader import PageData
from demo.page_loader import EmptyPageLoader
from tests.util import random_string


def create_empty_page_loader(*, url_repo: Address | None = None,
                             load_page: Callable[[str], PageData] | None = None) -> ActorTester:
    url_repo = url_repo if url_repo is not None else Address(f"$.tester.{random_string()}")

    if load_page is None:
        def load_page(_: str) -> PageData:
            return PageData("https://example.com/1234", "<html>abcdefg</html>")

    return ActorTester(EmptyPageLoader.create(url_repo, load_page))


def _default_load_page(_: str) -> PageData: return PageData("", "")
