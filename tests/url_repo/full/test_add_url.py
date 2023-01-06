from tests.url_repo.base.assertion import assert_acknowledge_add_url
from tests.url_repo.full.factory import create_full_url_repo


def test_should_acknowledge_add_url():
    assert_acknowledge_add_url(create_full_url_repo(urls=["https://example.com/0"]))
