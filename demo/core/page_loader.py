from dataclasses import dataclass

from lyrid import Message


@dataclass
class GetPage(Message):
    subscription_key: str


@dataclass
class SubscribePage(Message):
    subscription_key: str


@dataclass
class PageData(Message):
    url: str
    content: str
