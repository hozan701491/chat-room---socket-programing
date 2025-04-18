import socket
from queue import Queue

class Client(socket.socket):
    def __init__(
        self, family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0, fileno=None
    ):
        super().__init__(family, type, proto, fileno)
        self.recv_buff = Queue()
        self.send_buff = Queue()
        self.username  = str(self.fileno())

    def accept(self):
        fd, addr = self._accept()
        sock = Client(self.family, self.type, self.proto, fileno=fd)
        return sock, addr

    def __repr__(self):
        return repr(self.username)
    
    def __hash__(self):
        return hash(self.username)
    
    def __eq__(self, __value):
        return hash(__value) == hash(self)



