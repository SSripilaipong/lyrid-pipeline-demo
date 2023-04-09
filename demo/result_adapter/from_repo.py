from dataclasses import dataclass

from lyrid import Actor, use_switch, switch, Address

from demo.core.result_collector import GetResult, ResultData
from demo.core.url_repo import GetUrl, UrlData


@use_switch
@dataclass
class RepoResultAdapter(Actor):
    url_repo: Address
    collector: Address | None = None

    @switch.message(type=GetResult)
    def request_result(self, sender: Address):
        self.tell(self.url_repo, GetUrl())
        self.collector = sender

    @switch.message(type=UrlData)
    def url_data(self, message: UrlData):
        if self.collector is not None:
            self.tell(self.collector, ResultData(message.url))


def create_repo_result_adapter(url_repo: Address) -> RepoResultAdapter:
    return RepoResultAdapter(url_repo=url_repo)
