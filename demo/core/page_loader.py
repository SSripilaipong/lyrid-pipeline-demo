from dataclasses import dataclass

from lyrid import Message


@dataclass
class GetPage(Message):
    pass
