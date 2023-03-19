from lyrid.testing import ActorTester

from demo.url_repo import EmptyUrlRepo


def create_empty_url_repo(*, buffer_size: int = None) -> ActorTester:
    buffer_size = buffer_size if buffer_size is not None else 123
    return ActorTester(EmptyUrlRepo.create(buffer_size))
