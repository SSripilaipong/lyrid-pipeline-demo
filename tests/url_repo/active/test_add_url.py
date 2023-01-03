from lyrid.testing import ActorTester

from demo.url_repo import ActiveUrlRepo
from tests.url_repo.base.assertion import assert_acknowledge_add_url


def test_should_allow_actor_to_add_url():
    assert_acknowledge_add_url(ActorTester(ActiveUrlRepo()))
