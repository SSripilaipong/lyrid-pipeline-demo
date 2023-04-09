from dataclasses import dataclass

from lyrid import Actor, use_switch, switch, Address

from demo.core.page_loader import GetPage, PageData
from demo.core.result_collector import GetResult, ResultData


@use_switch
@dataclass
class LoaderResultAdapter(Actor):
    loader: Address
    collector: Address | None = None

    @switch.message(type=GetResult)
    def request_result(self, sender: Address):
        self.tell(self.loader, GetPage())
        self.collector = sender

    @switch.message(type=PageData)
    def page_data(self, message: PageData):
        if self.collector is not None:
            self.tell(self.collector, ResultData(message.content))


def create_loader_result_adapter(loader: Address) -> LoaderResultAdapter:
    return LoaderResultAdapter(loader=loader)
