import uuid

from lyrid import Address
from lyrid.testing import ActorTester

from demo.core.url_repo import AddUrl, GetUrl


def add_url(tester: ActorTester, url: str, *, by: Address | None = None):
    by = by or Address(f"$.tester.{random_string()}")

    tester.simulate.tell(AddUrl(url), by=by)


def get_url(tester: ActorTester, *, by: Address | None = None):
    by = by or Address(f"$.tester.{random_string()}")

    tester.simulate.tell(GetUrl(), by=by)


def random_string() -> str:
    return uuid.uuid4().hex
