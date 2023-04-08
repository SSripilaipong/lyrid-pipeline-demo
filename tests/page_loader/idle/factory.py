from lyrid import Address
from lyrid.testing import ActorTester

from demo.page_loader import IdlePageLoader
from tests.util import random_address


def create_idle_page_loader(*, url_repo: Address | None = None, buffer_size: int | None = None) -> ActorTester:
    url_repo = url_repo if url_repo is not None else random_address()
    buffer_size = buffer_size if buffer_size is not None else 999
    return ActorTester(IdlePageLoader.create(url_repo, buffer_size))
