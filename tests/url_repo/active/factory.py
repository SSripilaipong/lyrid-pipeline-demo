from typing import List

from lyrid import Address
from lyrid.testing import ActorTester

from demo.core.url_repo import SubscribeUrlData
from demo.url_repo import ExhaustedUrlRepo
from tests.url_repo.action import add_url


def create_active_url_repo(*, urls: List[str], subscribers: List[str] | None = None,
                           default_address: Address | None = None) -> ActorTester:
    assert len(urls) > 0
    subscribers = subscribers or []
    default_address = default_address or Address("$")

    tester = ActorTester(ExhaustedUrlRepo(123))
    for url in urls:
        add_url(tester, url, ref_id=url, by=default_address)

    for subscription in subscribers:
        tester.simulate.tell(SubscribeUrlData(subscription), by=default_address)
    tester.capture.clear_messages()

    return tester
