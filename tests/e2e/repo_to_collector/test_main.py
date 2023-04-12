import multiprocessing as mp
import time

import pytest
from lyrid import ActorSystem

from demo.core import common
from demo.core.url_repo import AddUrls
from demo.result_adapter import create_repo_result_adapter
from demo.result_collector import create_result_collector
from demo.url_repo import create_url_repo
from tests.util import random_url


@pytest.mark.e2e
def test_main():
    result_queue = mp.Manager().Queue()
    system = ActorSystem()

    try:
        url_repo = system.spawn(create_url_repo(buffer_size=10), initial_message=common.Start())
        adapter = system.spawn(create_repo_result_adapter(url_repo))
        system.spawn(create_result_collector([adapter], buffer_size=2, save=result_queue.put),
                     initial_message=common.Start())

        system.tell(url_repo, AddUrls([random_url() for _ in range(20)]))
        time.sleep(0.1)

        collected_results = []
        while len(collected_results) < 10:
            for result in result_queue.get(timeout=3):
                collected_results.append(result)

        system.tell(url_repo, AddUrls([random_url() for _ in range(20)]))

        collected_results = []
        while len(collected_results) < 10:
            for result in result_queue.get(timeout=3):
                collected_results.append(result)

    finally:
        system.force_stop()
