from dataclasses import dataclass

from lyrid import Message


@dataclass
class AddUrl(Message):
    url: str
    ref_id: str


@dataclass(frozen=True)
class AddUrlAck(Message):
    ref_id: str
