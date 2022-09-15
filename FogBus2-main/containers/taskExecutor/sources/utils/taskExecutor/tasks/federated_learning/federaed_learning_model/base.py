import time

from .base_model_abstract import base_model_abstract
from .datawarehouse import model_warehouse
from ..communicate.router import router_factory, ftp_server_factory, receive_file
import threading

import os
from pathlib import Path

import inspect


class base_model(base_model_abstract):

    def __init__(self):
        # model relationship handle
        self._name = "bas"
        self.uuid = model_warehouse().set(self)
        self.version = 1
        self.client = []
        self._client_waiting_list = []
        #self.client_lock = threading.Lock()
        self.server = []
        self._server_waiting_list = []
        #self.server_lock = threading.Lock()
        self.peer = []
        self._peer_waiting_list = []
        #self.peer_lock = threading.Lock()

        # model transmission
        # mode - version - data
        #self.export_lock = {"i": threading.Lock(), "f": threading.Lock()}
        self.export_cache = {"i": [0, None], "f": [0, None]}

        self.remote_fetch_model_credential = {"p": {}, "s": {}, "c": {}}
        #self.remote_fetch_model_credential_lock = {"p": threading.Lock(), "s": threading.Lock(), "c": threading.Lock()}

        self.client_model = {}
        #self.client_model_lock = threading.Lock()
        self.peer_model = {}
        #self.peer_model_lock = threading.Lock()
        self.server_model = {}
        #self.server_model_lock = threading.Lock()
        #self.additional_set_up()

    def additional_set_up(self):
        self.client_lock = threading.Lock()
        self.server_lock = threading.Lock()
        self.peer_lock = threading.Lock()
        self.export_lock = {"i": threading.Lock(), "f": threading.Lock()}
        self.remote_fetch_model_credential_lock = {"p": threading.Lock(), "s": threading.Lock(), "c": threading.Lock()}
        self.client_lock = threading.Lock()
        self.peer_model_lock = threading.Lock()
        self.server_model_lock = threading.Lock()

    def export(self):
        return self.__dict__

    """
    Functions to transmit model
    1. fetch_server/fetch_client/fetch_peer(local_dest)
    2. can_fetch
    3. export_model(local_dest): return (type, data)    local_dest = None (i mode) | local_dest = file_path (f) mode
      type 'i' - the model (pickle based tuple)
      type 'f' - credential to load the model (ftp login credential)
    4. push_model
    5. import_model(type, data, dest)
    """

    """
    END-----------------------------------------------------------------------------------
    """

    """
    f - fetch
    s : as server | c : as client | p : as peer
    """

    def fetch_client(self, client_model_ptr, dest=None):
        router = router_factory.get_default_router()
        addr, model_id, version = client_model_ptr
        router.send(addr, "communicatfs___", (self.uuid, version, model_id, dest))

    def fetch_peer(self, peer_model_ptr, dest=None):
        router = router_factory.get_default_router()
        addr, model_id, version = peer_model_ptr
        router.send(addr, "communicatfp___", (self.uuid, version, model_id, dest))

    def fetch_server(self, server_model_ptr, dest=None):
        router = router_factory.get_default_router()
        addr, model_id, version = server_model_ptr
        router.send(addr, "communicatfc___", (self.uuid, version, model_id, dest))

    def can_fetch(self, remote_ptr, role):  # check remote_ptr in self stored address ignoring version
        ignore_third = lambda x: [d[:2] for d in x]
        dic = {"s": ignore_third(self.server), "c": ignore_third(self.client), "p": ignore_third(self.peer)}
        return remote_ptr[:2] in dic[role]

    def export_model(self, mode="f", file_extension=".txt"):
        if self.version == self.export_cache[mode][0]:
            return mode, self.export_cache[mode][1]
        if not self.export_lock[mode].locked() and self.export_lock[mode].acquire():
            if mode == "f":
                file_dir = os.path.dirname(inspect.getsourcefile(router_factory)) + "/tmp/"
                file_name = self.uuid + file_extension
                f = open(file_dir + file_name, "w+")
                f.write(self.uuid)
                f.close()
                print()
                self.export_cache[mode][0] = self.version
                self.export_cache[mode][1] = file_name
            if mode == "i":
                self.export_cache[mode][0] = self.version
                self.export_cache[mode][1] = (self.uuid,)
        else:
            while self.export_lock[mode].locked():
                time.sleep(0.01)
        return mode, self.export_cache[mode][1]

    def push_model(self, remote_ptr, role, data, remote_dest):
        ftp_server, router = ftp_server_factory.get_default_ftp_server(), router_factory.get_default_router()
        addr, model_id, _ = remote_ptr
        _, password = ftp_server.add_temp_user(model_id+"_"+self.uuid)
        router.send(addr, "communicatp" + role + "___", (self.uuid, self.version, model_id, remote_dest, data +
                                                         (password, ftp_server.addr)))

    def import_model(self, role, data, dest, remote_ptr):
        self.remote_fetch_model_credential_lock[role].acquire()
        dic = self.remote_fetch_model_credential[role]
        dic[remote_ptr[:2]] = (data, dest)
        self.remote_fetch_model_credential_lock[role].release()

    def can_import(self, role, data, dest, remote_ptr):
        return True

    def fetch_model(self, role, dest, ptr):
        _lock, _dic = None, None
        if role == "s": _lock, _dic = self.server_model_lock, self.server_model
        if role == "p": _lock, _dic = self.peer_model_lock, self.peer_model
        if role == "c": _lock, _dic = self.client_model_lock, self.client_model
        ptr = ptr[:2]
        data = self.remote_fetch_model_credential[role][ptr]
        if dest: (mode, remote_file_path, password, server_addr), _ = data
        else: (mode, remote_file_path, password, server_addr), dest = data
        if not dest: dest = os.path.dirname(inspect.getsourcefile(router_factory)) + "/tmp/" + self.uuid + "_" + role + "_" + remote_file_path # remote_file_name
        receive_file(server_addr, remote_file_path, dest, self.uuid + "_" + ptr[1], password)
        _lock.acquire()
        _dic[ptr] = dest
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
    END-----------------------------------------------------------------------------------
    """
