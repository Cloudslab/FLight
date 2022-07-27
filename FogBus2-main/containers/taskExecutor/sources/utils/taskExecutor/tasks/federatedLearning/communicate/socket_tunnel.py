import socket
from threading import Thread
from .handler.base_handler import base_handler


class tunnel:
    __slots__ = ["socketI", "socketO", "handlers"]

    def __new__(cls, ip, port, *args, **kwargs):
        if (not isinstance(ip, str)) or (not isinstance(port, int)):
            return None
        return super(tunnel, cls).__new__(cls, *args, **kwargs)

    def __init__(self, ip, port):
        self.socketI = None
        self.socketO = []
        self.handlers = {
            b"register": base_handler()
        }
        self.socketI = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.socketI.bind((ip, port))
            self.socketI.listen()
            Thread(target=self.handle).start()
        except:
            self.socketI = None

    def handle(self):
        count = 2
        while True:
            conn, addr = self.socketI.accept()
            event = conn.recv(8)
            if event in self.handlers:
                Thread(target=self.handlers[event], args=(conn, addr, self, )).start()
            else:
                count -= 1
            if count == 0:
                break
    """
    def send(self, tag, id, data):
        if id < len(self.socketO):
            return

        try:

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(self.socketO[id])
                s.send(tag+data)
        except:
            return
    """


    def __del__(self):
        if self.socketI:
            self.socketI.close()
