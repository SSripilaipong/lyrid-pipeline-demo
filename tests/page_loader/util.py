from demo.core.page_loader import PageData
from tests.util import random_url, random_html_content


def random_page_data() -> PageData:
    return PageData(url=random_url(), content=random_html_content())
