from tests.url_repo.active.factory import create_active_url_repo_tester_with_urls
from tests.url_repo.base.assertion import assert_acknowledge_add_url


def test_should_allow_actor_to_add_url():
    assert_acknowledge_add_url(create_active_url_repo_tester_with_urls(["https://example.com"]))
