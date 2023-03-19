from demo.url_repo import EmptyUrlRepo, FullUrlRepo, ActiveUrlRepo
from tests.url_repo.action import get_url, add_urls
from tests.url_repo.active.factory import create_active_url_repo


def test_should_become_empty_when_all_urls_have_been_retrieved():
    tester = create_active_url_repo(urls=["https://example.com/0", "https://example.com/1"])

    get_url(tester)
    assert isinstance(tester.current_actor, ActiveUrlRepo)

    get_url(tester)
    assert isinstance(tester.current_actor, EmptyUrlRepo)


def test_should_become_full_when_number_of_urls_reached_the_buffer_size():
    tester = create_active_url_repo(buffer_size=2, urls=["https://example.com/0"])

    add_urls(tester, ["https://example.com/1", "https://example.com/2"])
    assert isinstance(tester.current_actor, FullUrlRepo)
