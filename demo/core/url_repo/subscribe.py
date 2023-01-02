from dataclasses import dataclass

from lyrid import Message


class SubscribeUrlData(Message):
    pass


@dataclass
class SubscribeUrlDataAck(Message):
    pass
