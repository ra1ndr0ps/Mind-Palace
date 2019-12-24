import struct
import datetime as dt
import threading
from .utils import Listener


HEADER_FORMAT = 'LLI'
HEADER_SIZE = struct.calcsize('LLI')


class Handler(threading.Thread):
    write_lock = threading.Lock()

    def __init__(self, connection, data_dir):
        super().__init__()
        self.connection = connection
        self.data_dir = data_dir

    def run(self):
        data = self.connection.receive(HEADER_SIZE)
        user_id, timestamp, size = struct.unpack(HEADER_FORMAT, data)
        timestamp = dt.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        data = self.connection.receive(size)
        self.connection.close()

        thought = f'{data}'
        year_month_day, hour = timestamp.split(' ')
        p = self.data_dir / f"{user_id}"
        p.mkdir(parents=True, exist_ok=True)
        filename = year_month_day + "_" + "-".join(hour.split(':')) + ".txt"
        filepath = p / filename
        if filepath.exists():
            thought = '\n' + thought
        Handler.write_lock.acquire()
        try:
            with filepath.open("a+", encoding="utf-8") as f:
                f.write(thought)
        finally:
            Handler.write_lock.release()


def run_server(address, data_dir):
    ip, port = address[0], address[1]
    listener = Listener(port, ip)
    listener.start()
    while True:
        client = listener.accept()
        handler = Handler(client, data_dir)
        handler.start()
