from dataclasses import dataclass

from lyrid import Message


@dataclass
class GetPage(Message):
    pass


@dataclass
class SubscribePage(Message):
    pass


@dataclass
class PageData(Message):
    url: str
    content: str
