from typing import List

from lyrid import Address
from lyrid.testing import ActorTester

from demo.core.url_repo import SubscribeUrlData
from demo.url_repo import FullUrlRepo


def create_full_url_repo(*, subscribers: List[str] | None = None,
                         default_address: Address | None = None) -> ActorTester:
    subscribers = subscribers or []
    default_address = default_address or Address("$.tester.default")

    tester = ActorTester(FullUrlRepo())

    for subscription in subscribers:
        tester.simulate.tell(SubscribeUrlData(subscription), by=default_address)
    tester.capture.clear_messages()

    return tester
