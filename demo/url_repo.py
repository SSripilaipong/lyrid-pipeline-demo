import os
import sqlite3
from contextlib import suppress
from typing import Dict

from lyrid import StatefulActor, Switch, Address, field, Reply, Ask

from demo.core import common
from demo.core.url_repo import *


class UrlRepo(StatefulActor):
    subscriber_tracking: Dict[Address, int] = field(default_factory=dict)

    db_file: str = "data/url_repo.db"
    db_conn: sqlite3.Connection = None
    db_cursor: sqlite3.Cursor = None

    switch = Switch()
    on_receive = switch.on_receive

    @switch.message(type=common.Start)
    def start(self, _: Address, __: common.Start):
        self.db_conn = sqlite3.connect(self.db_file)
        self.db_cursor = self.db_conn.cursor()

        self.db_cursor.execute("CREATE TABLE UrlData(url TEXT, PRIMARY KEY (url))")
        self.db_conn.commit()

    @switch.message(type=Ask)
    def user_interact(self, sender: Address, message: Ask):
        match message.message:
            case common.Stop():
                self.db_cursor.close()
                self.db_conn.close()
                with suppress(FileNotFoundError):
                    os.remove(self.db_file)

        self.tell(sender, Reply(common.Ok(), ref_id=message.ref_id))

    @switch.message(type=SubscribeUrlData)
    def subscribe(self, sender: Address, _: SubscribeUrlData):
        if sender not in self.subscriber_tracking:
            self.subscriber_tracking[sender] = -1

        self.tell(sender, SubscribeUrlDataAck())

    @switch.message(type=AddUrl)
    def add_url(self, sender: Address, message: AddUrl):
        pass
