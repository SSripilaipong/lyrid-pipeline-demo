import uuid
from typing import List

from lyrid import Address
from lyrid.testing import ActorTester

from demo.core.url_repo import AddUrls, GetUrl


def add_urls(tester: ActorTester, urls: List[str], *, by: Address | None = None):
    by = by or Address(f"$.tester.{random_string()}")

    tester.simulate.tell(AddUrls(urls), by=by)


def get_url(tester: ActorTester, *, by: Address | None = None):
    by = by or Address(f"$.tester.{random_string()}")

    tester.simulate.tell(GetUrl(), by=by)


def random_string() -> str:
    return uuid.uuid4().hex
