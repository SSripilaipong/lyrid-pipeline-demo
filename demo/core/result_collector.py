from dataclasses import dataclass

from lyrid import Message


@dataclass
class ResultData(Message):
    content: str


@dataclass
class GetResult(Message):
    ...
