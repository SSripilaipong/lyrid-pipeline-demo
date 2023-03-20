from typing import List

from lyrid import Address
from lyrid.testing import ActorTester

from demo.core.url_repo import AddUrls, GetUrl
from tests.util import random_address


def add_urls(tester: ActorTester, urls: List[str], *, by: Address | None = None):
    by = by or random_address()

    tester.simulate.tell(AddUrls(urls), by=by)


def get_url(tester: ActorTester, *, by: Address | None = None):
    by = by or random_address()

    tester.simulate.tell(GetUrl(), by=by)
