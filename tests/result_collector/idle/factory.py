from lyrid.testing import ActorTester

from demo.result_collector.idle import IdleResultCollector


def create_idle_result_collector() -> ActorTester:
    return ActorTester(IdleResultCollector())
