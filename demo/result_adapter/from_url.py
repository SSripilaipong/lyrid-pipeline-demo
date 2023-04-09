from dataclasses import dataclass

from lyrid import Actor, use_switch, switch, Address

from demo.core.result_collector import GetResult, ResultData
from demo.core.url_repo import GetUrl, UrlData


@use_switch
@dataclass
class UrlRepoResultAdapter(Actor):
    url_repo: Address
    collector: Address | None = None

    @switch.message(type=GetResult)
    def request_result(self, sender: Address):
        self.tell(self.url_repo, GetUrl())
        self.collector = sender

    @switch.message(type=UrlData)
    def url_data(self, message: UrlData):
        self.tell(self.collector, ResultData(message.url))


def create_result_adapter_from_url(url_repo: Address) -> 'UrlRepoResultAdapter':
    return UrlRepoResultAdapter(url_repo=url_repo)
