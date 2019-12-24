import socket
import datetime as dt
from . import Thought
from .utils import Connection


def upload_thought(address, user_id, thought):
    conn = socket.socket()
    client = Connection(conn)
    time = dt.datetime.now()
    thought = Thought(user_id, time, thought)
    msg = thought.serialize()
    client.send(msg)
    client.close()
    return
