import time

from lyrid import ActorSystem

from demo.core import common
from demo.url_repo import ActiveUrlRepo


def main():
    system = ActorSystem()
    url_repo = system.spawn(ActiveUrlRepo(), initial_message=common.Start())
    time.sleep(1)

    print(system.ask(url_repo, common.Stop()))
    system.force_stop()


if __name__ == "__main__":
    main()
