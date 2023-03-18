import uuid

from lyrid import Address
from lyrid.testing import ActorTester

from demo.core.url_repo import AddUrl, GetUrl


def add_url(tester: ActorTester, url: str, *, ref_id: str | None = None, by: Address | None = None):
    ref_id = ref_id or random_string()
    by = by or Address(f"$.tester.{random_string()}")

    tester.simulate.tell(AddUrl(url, ref_id=ref_id), by=by)


def get_url(tester: ActorTester, *, subscription: str | None = None, by: Address | None = None):
    by = by or Address(f"$.tester.{random_string()}")

    if subscription is None:
        subscription = random_string()

    tester.simulate.tell(GetUrl(subscription), by=by)


def random_string() -> str:
    return uuid.uuid4().hex
