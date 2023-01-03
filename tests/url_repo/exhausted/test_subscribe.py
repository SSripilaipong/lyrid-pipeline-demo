from tests.url_repo.base.assertion import assert_acknowledge_subscription
from tests.url_repo.exhausted.factory import create_exhausted_url_repo


def test_should_acknowledge_subscription():
    assert_acknowledge_subscription(create_exhausted_url_repo())
