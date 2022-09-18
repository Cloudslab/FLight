import time

from .base_model_abstract import base_model_abstract
from .datawarehouse import model_warehouse
from ..communicate.router import router_factory, ftp_server_factory, receive_file
import threading

import os
import ntpath

import inspect


class base_model(base_model_abstract):

    def __init__(self):
        # model relationship handle
        self._name = "bas"
        self.uuid = model_warehouse().set(self)
        self.version = 0
        self.client = []
        self._client_waiting_list = []
        self.client_lock = threading.Lock()
        self.server = []
        self._server_waiting_list = []
        self.server_lock = threading.Lock()
        self.peer = []
        self._peer_waiting_list = []
        self.peer_lock = threading.Lock()

        # model transmission
        self.export_lock = {"i": threading.Lock(), "f": threading.Lock()}
        self.export_cache = {"i": [-1, None], "f": [-1, None]}
        self.dummy_content = self.uuid + " " + str(self.version) + " created at " + str(time.ctime(time.time())) + "\n"
        self.export_model("i")
        self.export_model("f")

        self.remote_fetch_model_credential = {"p": {}, "s": {}, "c": {}}
        self.remote_fetch_model_credential_lock = {"p": threading.Lock(), "s": threading.Lock(), "c": threading.Lock()}

        self.client_model = {}
        self.client_model_lock = threading.Lock()
        self.peer_model = {}
        self.peer_model_lock = threading.Lock()
        self.server_model = {}
        self.server_model_lock = threading.Lock()

    def export(self):
        # return self.__dict__
        return {"uuid": self.uuid, "client": self.client, "server": self.server, "peer": self.peer}

    """
    Server - Client
    1. Server call client to train
    2. Client send back with credential
    3. Server
    """



    """
    Functions to transmit model
    """

    def fetch_client(self, client_model_ptr):
        router = router_factory.get_default_router()
        addr, model_id, version = client_model_ptr
        router.send(addr, "communicatfs___", (self.uuid, version, model_id, self.version))

    def fetch_peer(self, peer_model_ptr):
        router = router_factory.get_default_router()
        addr, model_id, version = peer_model_ptr
        router.send(addr, "communicatfp___", (self.uuid, version, model_id, self.version))

    def fetch_server(self, server_model_ptr):
        router = router_factory.get_default_router()
        addr, model_id, version = server_model_ptr
        router.send(addr, "communicatfc___", (self.uuid, version, model_id, self.version))

    def can_fetch(self, remote_ptr, role):  # check remote_ptr in self stored address ignoring version
        ignore_third = lambda x: [d[:2] for d in x]
        dic = {"s": ignore_third(self.get_server()), "c": ignore_third(self.get_client()), "p": ignore_third(self.get_peer())}
        return remote_ptr[:2] in dic[role]

    def give_fetch_credential(self, remote_ptr, mode="f"):
        ftp_server = ftp_server_factory.get_default_ftp_server()
        _, cache = self.export_cache[mode]
        addr, model_id, remote_version = remote_ptr
        username, password = ftp_server.add_temp_user(model_id + "_" + self.uuid)
        # create a user whose username is remote model's id
        return cache, username, password, ftp_server.addr, self.version, remote_version

    def _export_model(self, export_file_path):
        f = open(export_file_path, "w+")
        f.write(self.dummy_content)
        f.close()

    def export_model(self, mode="f", file_extension=".txt"):
        if self.version == self.export_cache[mode][0]: return
        if not self.export_lock[mode].locked() and self.export_lock[mode].acquire():
            if self.version > self.export_cache[mode][0]:
                # between checking version and acquire lock other thread may finish exporting, this can make sure
                # model is only exported once at a time
                if mode == "f":
                    export_dir = os.path.dirname(inspect.getsourcefile(router_factory)) + "/tmp/"
                    export_file_name = self.uuid + "_" + str(self.version) + file_extension
                    self._export_model(export_dir + export_file_name)
                    self.export_cache[mode] = [self.version, export_file_name]
                if mode == "i":
                    self.export_cache[mode] = [self.version, self.dummy_content]
            self.export_lock[mode].release()

    def send_download_credential(self, remote_ptr, role, credential):
        router = router_factory.get_default_router()
        addr, model_id, _ = remote_ptr
        router.send(addr, "communicatp" + role + "___", (self.uuid, model_id, credential))

    def save_download_model_credential(self, remote_ptr, role, credential):
        self.remote_fetch_model_credential_lock[role].acquire()
        self.remote_fetch_model_credential[role][remote_ptr[:2]] = credential
        self.remote_fetch_model_credential_lock[role].release()

    def remote_credential_valid(self, remote_ptr, role, credential):
        ignore_third = lambda x: [d[:2] for d in x]
        dic = {"s": ignore_third(self.server), "c": ignore_third(self.client), "p": ignore_third(self.peer)}
        return remote_ptr[:2] in dic[role]

    def download_model(self, remote_ptr, role, local_destination=None):
        _lock, _dic = None, None
        if role == "s": _lock, _dic = self.server_model_lock, self.server_model
        if role == "p": _lock, _dic = self.peer_model_lock, self.peer_model
        if role == "c": _lock, _dic = self.client_model_lock, self.client_model
        ptr = server_addr, remote_model_id = remote_ptr[:2]

        print(server_addr, remote_model_id)
        print(self.get_remote_fetch_model_credential(role).keys())
        if (server_addr, remote_model_id) not in self.get_remote_fetch_model_credential(role):
            return
        print(123)
        remote_file_name, username, password, ftp_addr, remote_version, self_version = self.remote_fetch_model_credential[role][ptr]
        if ptr not in _dic or _dic[ptr][1] < remote_version:
            if not local_destination:
                local_dir = os.path.dirname(inspect.getsourcefile(router_factory)) + "/tmp/"
                local_file_name = self.uuid + "_" + role + "_" + remote_file_name
                local_destination = local_dir + local_file_name

            receive_file(ftp_addr, remote_file_name, local_destination, username, password)
            _lock.acquire()
            _dic[ptr] = local_destination, remote_version, self.version
            _lock.release()
            self.remote_fetch_model_credential_lock[role].acquire()
            self.remote_fetch_model_credential[role].pop(ptr, None)
            self.remote_fetch_model_credential_lock[role].release()

    """
    Functions to handle relationships
    1. add_client/add_server/add_peer
    2. can_add(remote_ptr)
    3. ack_add(remote_ptr)
    4. _add_client/_add_server/_add_peer
    """

    def add_client(self, client_addr):
        router = router_factory.get_default_router()
        router.send(client_addr, "relation__as" + self._name, (self.uuid, self.version))

    def add_server(self, server_addr):
        router = router_factory.get_default_router()
        router.send(server_addr, "relation__ac" + self._name, (self.uuid, self.version))

    def add_peer(self, peer_addr):
        router = router_factory.get_default_router()
        router.send(peer_addr, "relation__ap" + self._name, (self.uuid, self.version))

    def can_add(self, remote_ptr, role):
        return True

    def add_ptr(self, remote_ptr, role):
        if role == "s":
            self._add_server(remote_ptr)
        if role == "c":
            self._add_client(remote_ptr)
        if role == "p":
            self._add_peer(remote_ptr)

    def _add_client(self, client_ptr):
        self.client_lock.acquire()
        self.client.append(client_ptr)
        self.client_lock.release()

    def _add_server(self, server_ptr):
        self.server_lock.acquire()
        self.server.append(server_ptr)
        self.server_lock.release()

    def _add_peer(self, peer_ptr):
        self.peer_lock.acquire()
        self.peer.append(peer_ptr)
        self.peer_lock.release()

    def ack_add(self, remote_ptr, role):
        router = router_factory.get_default_router()
        addr, model_id, version = remote_ptr
        router.send(addr, "relation__c" + role + "___", (self.uuid, self.version, model_id))

    """
    Getter Start
    """
    def get_client(self):
        return self.client.copy()

    def get_server(self):
        return self.server.copy()

    def get_peer(self):
        return self.peer.copy()

    def get_export_cache(self):
        return self.export_cache.copy()

    def get_remote_fetch_model_credential(self, role):
        return self.remote_fetch_model_credential.get(role).copy()

    def get_client_model(self):
        return self.client_model.copy()

    def get_server_model(self):
        return self.server_model.copy()

    def get_peer_model(self):
        return self.peer_model.copy()

    """
    Getter End
    """
