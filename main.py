import time

from lyrid import ActorSystem

from demo.core import common
from demo.core.url_repo import AddUrls
from demo.result_adapter import create_repo_result_adapter
from demo.result_collector import create_result_collector
from demo.url_repo import create_url_repo
from tests.util import random_url


def main():
    system = ActorSystem()
    url_repo = system.spawn(create_url_repo(buffer_size=10), initial_message=common.Start())
    adapter = system.spawn(create_repo_result_adapter(url_repo))
    system.spawn(create_result_collector(adapter, buffer_size=4, save=print), initial_message=common.Start())
    time.sleep(1)

    system.tell(url_repo, AddUrls([random_url() for _ in range(20)]))
    time.sleep(0.5)
    system.tell(url_repo, AddUrls([random_url() for _ in range(20)]))
    time.sleep(2)

    print("stopped:", system.ask(url_repo, common.Stop()))
    system.force_stop()


if __name__ == "__main__":
    main()
