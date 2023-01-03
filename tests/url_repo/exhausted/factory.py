from lyrid.testing import ActorTester

from demo.url_repo import ExhaustedUrlRepo


def create_exhausted_url_repo() -> ActorTester:
    return ActorTester(ExhaustedUrlRepo())
