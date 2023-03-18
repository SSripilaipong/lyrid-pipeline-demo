from dataclasses import dataclass

from lyrid import Message


@dataclass
class GetUrl(Message):
    pass


@dataclass(frozen=True)
class UrlData(Message):
    index: int
    data: str


@dataclass
class AddUrl(Message):
    url: str
    ref_id: str
