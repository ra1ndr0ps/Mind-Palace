import struct
import datetime as dt


_HEADER_FORMAT = 'LLI'
_HEADER_SIZE = struct.calcsize('LLI')


class Thought:

    def __init__(self, user_id, timestamp, thought):
        self.user_id = user_id
        self.timestamp = timestamp
        self.thought = thought

    def __repr__(self):
        return f'Thought(user_id={self.user_id!r}, timestamp={self.timestamp!r}, thought={self.thought!r})'

    def __str__(self):
        return f'[{self.timestamp:%Y-%m-%d %H:%M:%S}] user {self.user_id}: {self.thought}'

    def __eq__(self, other):
        if not isinstance(other, Thought):
            return False
        return self.user_id == other.user_id and self.timestamp == other.timestamp and self.thought == other.thought

    def serialize(self):
        header = struct.pack(_HEADER_FORMAT, self.user_id, int(self.timestamp.timestamp()), len(self.thought))
        return header + self.thought.encode()

    def deserialize(data):
        user_id, timestamp, size = struct.unpack(_HEADER_FORMAT, data[:_HEADER_SIZE])
        timestamp = dt.datetime.fromtimestamp(timestamp)
        thought = data[_HEADER_SIZE:].decode()
        return Thought(user_id, timestamp, thought)
