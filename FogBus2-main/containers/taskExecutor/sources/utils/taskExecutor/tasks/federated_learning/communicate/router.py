import socket
import ast
from threading import Thread
import queue
import pickle


ADDRESS_STRING_LEN = 40
EVENT_STRING_LEN = 10
MODEL_STRING_LEN = 5


class router_factory:
    routers = {}

    @classmethod
    def set_router(cls, addr):
        if addr not in cls.routers:
            try:
                new_router = router(addr[0], addr[1])
                new_router.start()
                cls.routers[addr] = new_router
            except Exception as e:
                print(e)
                print("Router Creation Fail")
                pass

    @classmethod
    def get_router(cls, addr):
        if addr in cls.routers:
            return cls.routers[addr]
        else:
            cls.set_router(addr)
            return cls.routers[addr]

    @classmethod
    def get_default_router(cls):
        if len(router_factory.routers):
            return router_factory.routers[list(router_factory.routers.keys())[0]]


class router:
    def __new__(cls, ip, port, *args, **kwargs):
        if (not isinstance(ip, str)) or (not isinstance(port, int)):
            return None
        return super(router, cls).__new__(cls, *args, **kwargs)

    def __init__(self, ip, port):
        self.socket = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((ip, port))

        self.sendingQueue = queue.Queue()

    def __del__(self):
        if self.socket:
            self.socket.close()

    def __str__(self):
        output = ""
        if self.socket: output += str(self.socket.getsockname())
        return output

    def add_handler(self, key, handler):
        self.__setattr__(key, handler)

    def start(self):
        Thread(target=self._dispatch).start()
        Thread(target=self._send).start()

    def _dispatch(self):
        self.socket.listen(5)
        while True:
            conn, _ = self.socket.accept()
            event = conn.recv(EVENT_STRING_LEN).decode("utf-8")
            model_type = conn.recv(MODEL_STRING_LEN).decode("utf-8")
            addr = ast.literal_eval(conn.recv(ADDRESS_STRING_LEN).decode("utf-8").rstrip())
            if hasattr(self, event) and callable(getattr(self, event)):
                Thread(target=getattr(self, event), args=(conn, addr, model_type, )).start()
            else:
                print("--------------------------------------")
                print(event)
                print(addr)
                print(model_type)
                print(pickle.loads(conn.recv(1000)))
                conn.close()

    def _send(self):
        while True:
            address, tag, data = self.sendingQueue.get()
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(address)
                s.sendall(tag.encode('utf-8')+(self.__str__().ljust(ADDRESS_STRING_LEN)).encode("utf-8") +
                          pickle.dumps(data))
                s.close()
            except Exception as e:
                print(e)

    def send(self, address, tag, data):
        self.sendingQueue.put((address, tag, data))
