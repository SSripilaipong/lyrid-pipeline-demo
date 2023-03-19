from lyrid import Address
from lyrid.testing import ActorTester

from demo.page_loader import IdlePageLoader
from tests.util import random_string


def create_idle_page_loader(*, url_repo: Address | None = None) -> ActorTester:
    url_repo = url_repo if url_repo is not None else Address(f"$.tester.{random_string()}")
    return ActorTester(IdlePageLoader.create(url_repo))
