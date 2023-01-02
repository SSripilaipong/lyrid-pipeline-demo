from dataclasses import dataclass

from lyrid import Actor, use_switch


@use_switch
@dataclass
class UrlRepo(Actor):
    pass
