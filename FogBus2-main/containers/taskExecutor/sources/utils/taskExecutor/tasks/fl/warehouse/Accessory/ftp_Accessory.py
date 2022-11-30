"""This file represents data stored as files on ftp server"""

from .abstract_Accessory import abstract_accessory
from collections import defaultdict
from ..storage_folder.folder_manager import folder_position
import os
import pickle
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import random
import string
from threading import Thread

def random_password(length):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))


class ftp_accessory(abstract_accessory):

    def __init__(self, addr):
        self._file_names = defaultdict(lambda: "")
        self.ftp_server_addr, self._ftp_server = ftp_accessory.start_ftp_server(addr)

    def set(self, args: dict, data_id: str = None):
        if not data_id:
            data_id = self.get_new_id()
        if "file_name" in args and "raw_data" in args:
            file_path = os.path.join(self._ftp_server.directory_path, args["file_name"])
            self.write_to_file(file_path, args["raw_data"])
            self._file_names[data_id] = args["file_name"]
        return data_id

    def get(self, args: dict, data_id: str):  # return credential to download from ftp server
        file_name = self._file_names.get(data_id)
        user_name = random_password(32)
        if file_name:
            user_name, password = self._ftp_server.add_temp_user(user_name)
            return self.ftp_server_addr, user_name, password, file_name
        else:
            return None

    @staticmethod
    def start_ftp_server(addr, retry=10):
        if not retry:
            return None
        try:
            ftp_server = _ftp_server(addr)
            ftp_server.start()
            return addr, ftp_server
        except Exception as e:
            return ftp_accessory.start_ftp_server((addr[0], addr[1]+1), retry-1)

    @staticmethod
    def write_to_file(file_path, data):
        f = open(file_path, "wb+")
        f.write(pickle.dumps(data))
        f.close()

    @staticmethod
    def read_from_file(file_path):
        f = open(file_path, "rb")
        data = pickle.loads(f.read())
        f.close()
        return data

# make sure one time login for given credential
class _handler(FTPHandler):
    def on_logout(self, username):
        self.authorizer.remove_user(username)


class _ftp_server:
    def __init__(self, address):  # (ip, port)
        self._handler = _handler
        self._handler.authorizer = DummyAuthorizer()
        self._address = address
        self._server = FTPServer(self._address, self._handler)
        self.directory_path = folder_position.ftp_folder()

    def start(self):
        Thread(target=self._server.serve_forever, args=()).start()

    def add_temp_user(self, user_name):
        if self._handler.authorizer.has_user(user_name):
            self._handler.authorizer.remove_user(user_name)
        temporary_password = random_password(32)
        self._handler.authorizer.add_user(user_name, temporary_password, self.directory_path, perm="lr")
        return user_name, temporary_password
