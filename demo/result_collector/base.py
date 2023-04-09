from dataclasses import dataclass

from lyrid import Actor


@dataclass
class ResultCollectorBase(Actor):
    buffer_size: int
