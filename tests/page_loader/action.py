from lyrid import Address
from lyrid.testing import ActorTester

from demo.core import common
from demo.core.page_loader import GetPage, PageData
from demo.core.url_repo import UrlData
from tests.page_loader.util import random_page_data
from tests.util import random_address, random_url, random_string


def start(tester: ActorTester):
    sender = random_address()

    tester.simulate.tell(common.Start(), by=sender)


def page_loading_completed(tester: ActorTester, *, page: PageData | None = None, task_id: str | None = None):
    page = page if page is not None else random_page_data()
    task_id = task_id if task_id is not None else random_string()

    tester.simulate.background_task_exit(task_id, return_value=page)


def get_page(tester: ActorTester, *, sender: Address | None = None):
    sender = sender if sender is not None else random_address()

    tester.simulate.tell(GetPage(), by=sender)


def receive_url_data(tester: ActorTester, *, url: str | None = None):
    sender = random_address()
    url = url if url is not None else random_url()

    tester.simulate.tell(UrlData(url), by=sender)
