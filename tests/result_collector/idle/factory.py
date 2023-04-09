from lyrid import Address
from lyrid.testing import ActorTester

from demo.result_collector.idle import IdleResultCollector
from tests.util import random_address


def create_idle_result_collector(*, processor: Address | None = None, buffer_size: int | None = None) -> ActorTester:
    processor = processor if processor is not None else random_address()
    buffer_size = buffer_size if buffer_size is not None else 999

    return ActorTester(IdleResultCollector.create(buffer_size=buffer_size, processor=processor))
