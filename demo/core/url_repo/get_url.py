from dataclasses import dataclass

from lyrid import Message


@dataclass
class GetUrlAfter(Message):
    subscription: str
    index: int


@dataclass
class UrlData(Message):
    index: int
    data: str
