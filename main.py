import time

from lyrid import ActorSystem

from demo.core import common
from demo.url_repo import create_url_repo


def main():
    system = ActorSystem()
    url_repo = system.spawn(create_url_repo(500), initial_message=common.Start())
    time.sleep(1)

    print("stopped:", system.ask(url_repo, common.Stop()))
    system.force_stop()


if __name__ == "__main__":
    main()
