from dataclasses import dataclass
from typing import List

from lyrid import Message


@dataclass
class GetUrl(Message):
    pass


@dataclass(frozen=True)
class UrlData(Message):
    url: str


@dataclass
class AddUrls(Message):
    urls: List[str]
