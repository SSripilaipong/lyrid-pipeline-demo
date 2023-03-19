from demo.url_repo import EmptyUrlRepo, ActiveUrlRepo, FullUrlRepo
from tests.url_repo.action import get_url, add_urls
from tests.url_repo.empty.factory import create_empty_url_repo


def test_should_become_active_when_no_waiting_actor_and_has_an_extra_url():
    tester = create_empty_url_repo()
    get_url(tester)

    add_urls(tester, ["https://example.com/0"])
    assert isinstance(tester.current_actor, EmptyUrlRepo)

    add_urls(tester, ["https://example.com/1"])
    assert isinstance(tester.current_actor, ActiveUrlRepo)


def test_should_become_full_when_no_waiting_actor_and_has_an_extra_url_reached_to_buffer_size():
    tester = create_empty_url_repo(buffer_size=2)
    assert isinstance(tester.current_actor, EmptyUrlRepo)

    add_urls(tester, ["https://example.com/0", "https://example.com/1"])
    assert isinstance(tester.current_actor, FullUrlRepo)
