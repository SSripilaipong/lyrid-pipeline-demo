from lyrid.testing import ActorTester

from demo.url_repo import EmptyUrlRepo


def create_empty_url_repo() -> ActorTester:
    return ActorTester(EmptyUrlRepo())
