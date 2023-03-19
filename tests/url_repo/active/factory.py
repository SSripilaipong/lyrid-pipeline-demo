from typing import List

from lyrid.testing import ActorTester

from demo.url_repo import ActiveUrlRepo


def create_active_url_repo(*, urls: List[str], buffer_size: int | None = None) -> ActorTester:
    assert len(urls) > 0
    buffer_size = buffer_size if buffer_size is not None else 123

    return ActorTester(ActiveUrlRepo.create(buffer_size, urls))
