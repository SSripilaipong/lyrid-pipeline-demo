from dataclasses import dataclass

from lyrid import Message


@dataclass
class GetUrl(Message):
    pass


@dataclass(frozen=True)
class UrlData(Message):
    url: str


@dataclass
class AddUrl(Message):
    url: str
