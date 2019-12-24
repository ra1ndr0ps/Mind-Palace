import socket


class Connection:

    def __init__(self, socket):
        self.socket = socket

    def __repr__(self):
        src_ip = self.socket.getsockname()
        target_ip = self.socket.getpeername()
        src_ip = src_ip[0] + ":" + str(src_ip[1])
        target_ip = target_ip[0] + ":" + str(target_ip[1])
        return f'<Connection from {src_ip} to {target_ip}>'

    def __enter__(self):
        return self

    def __exit__(self, exception, error, traceback):
        self.close()

    @classmethod
    def connect(cls, host, port):
        sock = socket.socket()
        sock.connect((host, port))
        return cls(sock)

    def receive(self, size):
        data = b''
        while len(data) < size:
            part = self.socket.recv(size - len(data))
            data += part
            if not part:
                raise Exception('Connection was closed before all data was received')
        return data

    def send(self, data):
        self.socket.sendall(data)

    def close(self):
        self.socket.close()
