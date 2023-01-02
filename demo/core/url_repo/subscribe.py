from dataclasses import dataclass

from lyrid import Message


@dataclass
class SubscribeUrlData(Message):
    subscription_key: str


@dataclass
class SubscribeUrlDataAck(Message):
    subscription_key: str
