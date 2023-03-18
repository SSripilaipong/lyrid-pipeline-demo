from demo.url_repo import ExhaustedUrlRepo
from tests.url_repo.action import get_url
from tests.url_repo.active.factory import create_active_url_repo


def test_should_become_exhausted_when_all_urls_have_been_retrieved():
    tester = create_active_url_repo(urls=["https://example.com/0", "https://example.com/1"])

    get_url(tester)
    assert not isinstance(tester.current_actor, ExhaustedUrlRepo)

    get_url(tester)
    assert isinstance(tester.current_actor, ExhaustedUrlRepo)
