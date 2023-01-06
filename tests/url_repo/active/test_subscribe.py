from tests.url_repo.active.factory import create_active_url_repo
from tests.url_repo.base.assertion import assert_acknowledge_subscription


def test_should_acknowledge_subscription():
    assert_acknowledge_subscription(create_active_url_repo(urls=["https://example.com"]))
