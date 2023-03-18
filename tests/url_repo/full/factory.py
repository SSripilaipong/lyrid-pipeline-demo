from typing import List

from lyrid.testing import ActorTester

from demo.url_repo import FullUrlRepo


def create_full_url_repo(*, urls: List[str]) -> ActorTester:
    tester = ActorTester(FullUrlRepo(len(urls), urls=urls))
    tester.capture.clear_messages()

    return tester
