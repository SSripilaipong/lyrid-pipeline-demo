from typing import Callable

from lyrid.testing import ActorTester


def assert_have_run_loading_background_task(tester: ActorTester, loading_task: Callable, url: str):
    tasks = tester.capture.get_background_tasks()
    assert len(tasks) == 1
    task_call = tasks[0]
    assert task_call.task == loading_task and task_call.args == (url,)
