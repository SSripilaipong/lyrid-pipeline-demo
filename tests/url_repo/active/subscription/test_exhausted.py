from demo.url_repo import ExhaustedUrlRepo
from tests.url_repo.action import get_url_after_index
from tests.url_repo.active.factory import create_active_url_repo


# noinspection DuplicatedCode
def test_should_become_exhausted_when_all_urls_have_been_retrieved():
    tester = create_active_url_repo(urls=["https://example.com/0", "https://example.com/1"], subscribers=["a"])

    get_url_after_index(tester, -1, subscription="a")
    get_url_after_index(tester, 0, subscription="a")

    assert isinstance(tester.current_actor, ExhaustedUrlRepo)
