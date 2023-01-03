from lyrid.testing import ActorTester

from demo.url_repo import EmptyUrlRepo
from tests.url_repo.base.assertion import assert_acknowledge_subscription


def test_should_acknowledge_subscription():
    assert_acknowledge_subscription(ActorTester(EmptyUrlRepo()))
