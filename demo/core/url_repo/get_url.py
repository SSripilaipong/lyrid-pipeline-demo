from dataclasses import dataclass

from lyrid import Message


@dataclass
class GetUrl(Message):
    subscription: str


@dataclass(frozen=True)
class UrlData(Message):
    index: int
    data: str
