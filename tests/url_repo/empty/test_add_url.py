from lyrid.testing import ActorTester

from demo.url_repo import EmptyUrlRepo
from tests.url_repo.base.assertion import assert_acknowledge_add_url


def test_should_acknowledge_add_url():
    assert_acknowledge_add_url(ActorTester(EmptyUrlRepo()))
