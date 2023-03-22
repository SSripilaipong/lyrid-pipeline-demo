from typing import Callable

from lyrid import Address
from lyrid.testing import ActorTester

from demo.page_loader import ActivePageLoader
from tests.util import random_string


def create_active_page_loader(*, url_repo: Address | None = None,
                              load_page: Callable[[str], str] | None = None) -> ActorTester:
    url_repo = url_repo if url_repo is not None else Address(f"$.tester.{random_string()}")

    if load_page is None:
        def load_page(_: str) -> str:
            return ""

    return ActorTester(ActivePageLoader.create(url_repo, load_page))
