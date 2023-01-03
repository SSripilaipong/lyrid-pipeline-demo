from typing import List

from lyrid import Address
from lyrid.testing import ActorTester

from demo.core.url_repo import AddUrl
from demo.url_repo import EmptyUrlRepo


def create_active_url_repo_tester_with_urls(urls: List[str]) -> ActorTester:
    assert len(urls) > 0

    tester = ActorTester(EmptyUrlRepo())
    for url in urls:
        tester.simulate.tell(AddUrl(url, ref_id=url), by=Address("$"))
    return tester
