from tests.url_repo.base.assertion import assert_acknowledge_add_url
from tests.url_repo.exhausted.factory import create_exhausted_url_repo


def test_should_acknowledge_add_url():
    assert_acknowledge_add_url(create_exhausted_url_repo())
