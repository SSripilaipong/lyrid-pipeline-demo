from typing import List

from lyrid import Address
from lyrid.testing import ActorTester

from demo.url_repo import EmptyUrlRepo
from tests.url_repo.action import add_urls


def create_active_url_repo(*, urls: List[str], default_address: Address | None = None) -> ActorTester:
    assert len(urls) > 0
    default_address = default_address or Address("$")

    tester = ActorTester(EmptyUrlRepo(123))
    add_urls(tester, urls, by=default_address)

    tester.capture.clear_messages()

    return tester
