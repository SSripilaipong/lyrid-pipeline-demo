from lyrid import Address
from lyrid.testing import ActorTester

from demo.result_collector.idle import IdleResultCollector
from tests.util import random_address


def create_idle_result_collector(*, processor: Address | None = None) -> ActorTester:
    processor = processor if processor is not None else random_address()

    return ActorTester(IdleResultCollector.create(processor=processor))
