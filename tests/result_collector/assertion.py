from typing import Callable, List

from lyrid.testing import ActorTester

from demo.core.result_collector import ResultData


def assert_have_run_saving_background_task(tester: ActorTester, save: Callable[[List[ResultData]], None],
                                           data: List[ResultData]):
    tasks = tester.capture.get_background_tasks()
    assert len(tasks) == 1
    task = tasks[0]
    assert task.task == save and task.args == (data,)
