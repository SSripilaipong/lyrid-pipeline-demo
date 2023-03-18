from lyrid.testing import ActorTester

from demo.url_repo import EmptyUrlRepo


def create_empty_url_repo() -> ActorTester:
    tester = ActorTester(EmptyUrlRepo(123))
    tester.capture.clear_messages()

    return tester
