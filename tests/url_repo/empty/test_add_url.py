from tests.url_repo.base.assertion import assert_acknowledge_add_url
from tests.url_repo.empty.factory import create_empty_url_repo


def test_should_acknowledge_add_url():
    assert_acknowledge_add_url(create_empty_url_repo())
