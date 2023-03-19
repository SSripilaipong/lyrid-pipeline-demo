from demo.url_repo import ActiveUrlRepo, FullUrlRepo, EmptyUrlRepo
from tests.url_repo.action import get_url, add_urls
from tests.url_repo.full.factory import create_full_url_repo


def test_should_become_active_after_send_one_url():
    tester = create_full_url_repo(urls=["https://example.com/0", "https://example.com/1"])
    add_urls(tester, ["https://example.com/2", "https://example.com/3"])  # should be ignored
    assert isinstance(tester.current_actor, FullUrlRepo)

    get_url(tester)
    assert isinstance(tester.current_actor, ActiveUrlRepo)


def test_should_become_empty_after_send_one_url_if_buffer_size_is_1():
    tester = create_full_url_repo(urls=["https://example.com/0"])
    add_urls(tester, ["https://example.com/2", "https://example.com/3"])  # should be ignored
    assert isinstance(tester.current_actor, FullUrlRepo)

    get_url(tester)
    assert isinstance(tester.current_actor, EmptyUrlRepo)
