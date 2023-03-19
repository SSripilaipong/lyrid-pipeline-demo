from typing import List

from lyrid.testing import ActorTester

from demo.url_repo import ActiveUrlRepo


def create_active_url_repo(*, urls: List[str]) -> ActorTester:
    assert len(urls) > 0

    return ActorTester(ActiveUrlRepo.create(123, urls))
