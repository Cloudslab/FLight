import socket
import ast
from threading import Thread
import queue
import pickle
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import os
import inspect
import string
import random
import ftplib

ADDRESS_STRING_LEN = 40
EVENT_STRING_LEN = 10
MODEL_STRING_LEN = 5
RAMDOM_PASSWORD = lambda l: ''.join(random.choice(string.ascii_lowercase) for i in range(l))


class router_factory:
    routers = {}

    @classmethod
    def set_router(cls, addr):
        if addr not in cls.routers:
            try:
                new_router = router(addr[0], addr[1])
                new_router.start()
                cls.routers[addr] = new_router
                return addr
            except Exception as e:
                return cls.set_router((addr[0], addr[1] + 1))

    @classmethod
    def get_router(cls, addr):
        if addr in cls.routers:
            return addr, cls.routers[addr]
        else:

            addr = cls.set_router(addr)
            return addr, cls.routers[addr]

    @classmethod
    def get_default_router(cls):
        if len(router_factory.routers):
            return router_factory.routers[list(router_factory.routers.keys())[0]]


class ftp_server_factory:
    ftp_servers = {}

    @classmethod
    def set_ftp_server(cls, addr):
        if addr not in cls.ftp_servers:
            try:
                new_ftp_server = ftp_server(addr)
                cls.ftp_servers[addr] = new_ftp_server
                new_ftp_server.start()
                return addr
            except Exception as e:
                return cls.set_ftp_server((addr[0], addr[1] + 1))

    @classmethod
    def get_ftp_server(cls, addr):
        if addr in cls.ftp_servers:
            return addr, cls.ftp_servers[addr]
        else:
            addr = cls.set_ftp_server(addr)
            return addr, cls.ftp_servers[addr]

    @classmethod
    def get_default_ftp_server(cls):
        if len(cls.ftp_servers):
            return cls.ftp_servers[list(cls.ftp_servers.keys())[0]]


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
            sub_event = conn.recv(MODEL_STRING_LEN).decode("utf-8")
            addr = ast.literal_eval(conn.recv(ADDRESS_STRING_LEN).decode("utf-8").rstrip())
            if hasattr(self, event) and callable(getattr(self, event)):
                Thread(target=getattr(self, event), args=(conn, addr, sub_event,)).start()
            else:

                y = 1
                y.sot()
                print("--------------------------------------")
                print(event)
                print(addr)
                print(sub_event)
                print(pickle.loads(conn.recv(1000)))
                conn.close()

    def _send(self):
        while True:
            address, tag, data = self.sendingQueue.get()
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(address)
                s.sendall(tag.encode('utf-8') + (self.__str__().ljust(ADDRESS_STRING_LEN)).encode("utf-8") +
                          pickle.dumps(data))
            except Exception as e:
                print(e)

    def send(self, address, event, data):
        self.sendingQueue.put((address, event, data))


class _handler(FTPHandler):
    def on_logout(self, username):
        self.authorizer.remove_user(username)


class ftp_server:
    def __init__(self, addr):
        self.handler = _handler
        self.handler.authorizer = DummyAuthorizer()
        self.addr = addr
        self.server = FTPServer(self.addr, self.handler)
        self.directory_path = os.path.dirname(inspect.getsourcefile(ftp_server)) + "/tmp/"

    def start(self):
        Thread(target=self.server.serve_forever, args=()).start()

    def add_temp_user(self, user_name):
        if self.handler.authorizer.has_user(user_name):
            self.handler.authorizer.remove_user(user_name)
        temporary_password = RAMDOM_PASSWORD(32)
        self.handler.authorizer.add_user(user_name, temporary_password, self.directory_path, perm="lr")
        return user_name, temporary_password


def receive_file(server_addr, server_path, dest_path, username, password):
    server = ftplib.FTP()
    server.connect(server_addr[0], server_addr[1])
    server.login(username, password)

    with open(dest_path, "wb") as file:
        server.retrbinary(f"RETR {server_path}", file.write)

    server.quit()
    server.close()
