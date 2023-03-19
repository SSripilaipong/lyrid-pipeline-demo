from demo.url_repo import EmptyUrlRepo, ActiveUrlRepo
from tests.url_repo.action import get_url, add_urls
from tests.url_repo.empty.factory import create_empty_url_repo


def test_should_become_active_when_no_waiting_actor_and_has_an_extra_url():
    tester = create_empty_url_repo()
    get_url(tester)

    add_urls(tester, ["https://example.com/0"])
    assert isinstance(tester.current_actor, EmptyUrlRepo)

    add_urls(tester, ["https://example.com/1"])
    assert isinstance(tester.current_actor, ActiveUrlRepo)
