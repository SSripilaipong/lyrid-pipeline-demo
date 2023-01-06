from tests.url_repo.base.assertion import assert_acknowledge_subscription
from tests.url_repo.full.factory import create_full_url_repo


def test_should_acknowledge_subscription():
    assert_acknowledge_subscription(create_full_url_repo(urls=["https://example.com/0"]))
