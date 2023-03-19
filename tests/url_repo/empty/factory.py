from lyrid.testing import ActorTester

from demo.url_repo import create_url_repo


def create_empty_url_repo() -> ActorTester:
    return ActorTester(create_url_repo(123))
