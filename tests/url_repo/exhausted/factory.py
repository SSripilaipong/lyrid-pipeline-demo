from lyrid.testing import ActorTester

from demo.url_repo import ExhaustedUrlRepo


def create_exhausted_url_repo() -> ActorTester:
    tester = ActorTester(ExhaustedUrlRepo(123))
    tester.capture.clear_messages()

    return tester
