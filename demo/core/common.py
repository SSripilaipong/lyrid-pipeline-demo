from dataclasses import dataclass

from lyrid import Message


@dataclass
class Start(Message):
    pass


@dataclass
class Stop(Message):
    pass
