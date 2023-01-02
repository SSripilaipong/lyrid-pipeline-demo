from dataclasses import dataclass

from lyrid import Message


@dataclass
class GetUrlAfter(Message):
    index: int


@dataclass
class UrlData(Message):
    index: int
    data: str


@dataclass
class UrlDataAck(Message):
    index: int
