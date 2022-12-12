from dataclasses import dataclass

from lyrid import Message


@dataclass
class GetUrlAfter(Message):
    order: int


@dataclass
class UrlData(Message):
    order: int
    data: str


@dataclass
class UrlDataAck(Message):
    order: int
