from tests.page_loader.action import receive_url_data
from tests.page_loader.empty.factory import create_empty_page_loader, _default_load_page


def test_should_run_page_loading_background_task_when_receiving_url_data():
    tester = create_empty_page_loader(load_page=_default_load_page)

    receive_url_data(tester, url="https://example.com/123")

    _assert_have_run_default_loading_background_task(tester, "https://example.com/123")


def _assert_have_run_default_loading_background_task(tester, url):
    tasks = tester.capture.get_background_tasks()
    assert len(tasks) == 1
    task_call = tasks[0]
    assert task_call.task == _default_load_page and task_call.args == (url,)
