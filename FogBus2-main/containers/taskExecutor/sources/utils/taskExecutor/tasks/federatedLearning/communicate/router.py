import socket
from threading import Thread


class router:
    def __new__(cls, ip, port, *args, **kwargs):
        if (not isinstance(ip, str)) or (not isinstance(port, int)):
            return None
        return super(router, cls).__new__(cls, *args, **kwargs)

    def __init__(self, ip, port):
        self.socketI = None
        self.socketI = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketI.bind((ip, port))

        self.socketO = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketO.bind((ip, port+1))

    def __del__(self):
        if self.socketI:
            self.socketI.close()
        if self.socketO:
            self.socketO.close()

    def __str__(self):
        output = ""
        if self.socketI: output += str(self.socketI.getsockname())
        if self.socketO: output += str(self.socketO.getsockname())
        return output

    def add_handler(self, key, handler):
        self.__setattr__(key, handler)

    def dispatch(self):
        Thread(target=self._dispatch).start()

    def _dispatch(self):
        self.socketI.listen()
        remain = 2
        while True and remain:
            conn, addr = self.socketI.accept()
            event = conn.recv(8).decode("utf-8")
            if hasattr(self, event) and callable(getattr(self, event)):
                Thread(target=getattr(self, event), args=(conn, addr,)).start()
            else:
                print(conn)
                print(addr)
                conn.close()
                remain -= 1

    def send(self, address, tag, data):
        if self.socketO:
            self.socketO.connect(address)
            buf = tag.encode("utf-8") + data
            self.socketO.sendall(buf)


if __name__ == "__main__":
    ro = router("127.0.0.1", 12345)
    ro.dispatch()
    print(ro)
