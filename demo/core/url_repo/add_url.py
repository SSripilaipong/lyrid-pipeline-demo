from dataclasses import dataclass

from lyrid import Message


@dataclass
class AddUrl(Message):
    url: str
    ref_id: str
