from . import Connection
import socket


class Listener:
    def __init__(self, port, host='0.0.0.0', backlog=1000, reuseaddr=True):
        self.port = port
        self.host = host
        self.backlog = backlog
        self.reuseaddr = reuseaddr
        self.listener = None

    def __repr__(self):
        return f'Listener(port={self.port}, host={self.host}, backlog={self.backlog}, reuseaddr={self.reuseaddr})'

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exception, error, traceback):
        self.stop()

    def start(self):
        self.listener = socket.socket()
        if self.reuseaddr:
            self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.listener.bind((self.host, self.port))
        except socket.error as e:
            if e.errno == errno.EADDRINUSE:
                print(f'ERROR: port {self.port} is already in use.')
            else:
                print(f'ERROR: {e}')
            return
        self.listener.listen(self.backlog)

    def accept(self):
        connection, address = self.listener.accept()
        return Connection(connection)

    def stop(self):
        self.listener.close()
