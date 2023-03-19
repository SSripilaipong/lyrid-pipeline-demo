from lyrid.testing import ActorTester

from demo.page_loader import IdlePageLoader


def create_idle_url_loader() -> ActorTester:
    return ActorTester(IdlePageLoader.create())
