from demo.url_repo import EmptyUrlRepo
from tests.url_repo.action import add_urls, get_url
from tests.url_repo.active.factory import create_active_url_repo


def test_should_not_add_urls_more_than_buffer_size():
    tester = create_active_url_repo(urls=["https://example.com/0"], buffer_size=2)
    add_urls(tester, ["https://example.com/1", "https://example.com/2"])

    get_url(tester)
    get_url(tester)
    assert isinstance(tester.current_actor, EmptyUrlRepo)

    tester.capture.clear_messages()

    get_url(tester)
    assert len(tester.capture.get_messages()) == 0
    assert isinstance(tester.current_actor, EmptyUrlRepo)
