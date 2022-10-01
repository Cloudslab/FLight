import time

from .base_model_abstract import base_model_abstract
from .datawarehouse import model_warehouse
from ..communicate.router import router_factory, ftp_server_factory, receive_file
import threading

import os
import ntpath

import inspect


class base_model(base_model_abstract):

    def __init__(self, export_at_creation=True):
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
        if export_at_creation:
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

        # during step, model cannot be exported
        self.model_lock = threading.Lock()
        self.waiting_client_lock = threading.Lock()
        self.waiting_client = {}  # key is client pointer, value is the version they had about this server

        self.synchronous_federate_minimum_client = 2
        self.client_model_cache = []  # using model lock (cache will only be touched during federation) so do not put an extra lock here

        # client selection module
        self.client_performance = {}
        self.cs_info = {
            "data_size": 0,
            "train_one_time": 0,
            "epoch_time": 0,
            "loading_time": 0
        }

        self.client_performance_lock = threading.Lock()
        self.time_allowed = float('inf')
        self.update_time_threshold = 5

    """
    Client Performance base Selection
    """
    def should_early_terminate(self, accuracy_list, terminate_threshold=1):
        reach_minimum_epoch = len(accuracy_list) >= 5
        not_update1, not_update2, not_update3, not_update4 = False, False, False, False
        if reach_minimum_epoch:
            not_update1 = (accuracy_list[-1] - accuracy_list[-2]) < terminate_threshold
            not_update2 = (accuracy_list[-2] - accuracy_list[-3]) < terminate_threshold
            not_update3 = (accuracy_list[-3] - accuracy_list[-4]) < terminate_threshold
            not_update4 = (accuracy_list[-4] - accuracy_list[-5]) < terminate_threshold
        return not_update1 and not_update2 and not_update3 and not_update4

    def should_update_time_allowed(self, new_accuracy, old_accuracy):
        return (new_accuracy - old_accuracy) < self.update_time_threshold and len(self.select_client()) != len(self.client)

    def update_time_allowed(self, step):
        l_current = len(self.select_client())
        if l_current != len(self.client):
            while len(self.select_client()) == l_current:
                self.time_allowed += step
                print("Update Triggerred")

    def update_client_performance(self, ptr, performance):
        self.client_performance_lock.acquire()
        for k in performance.keys():
            self.client_performance[ptr[:2]][k] = performance[k]
        self.client_performance_lock.release()

    def estimate_client_time(self, val):
        return val["train_one_time"] * val["data_size"] + val["loading_time"] + val["transmission_time"]

    def can_participate(self, ptr):
        have_ptr_statistics = ptr[:2] in self.client_performance.keys()
        fast_enough = self.estimate_client_time(self.client_performance[ptr[:2]]) <= self.time_allowed
        return (not have_ptr_statistics) or fast_enough

    def select_client(self):
        clients = self.get_client()
        res = [ele for ele in clients if self.can_participate(ele)]
        return res

    def export(self):
        # return self.__dict__
        return {"uuid": self.uuid, "client": self.client, "server": self.server, "peer": self.peer}

    """
    Server - Client
    1. Server call client to train
    2. Client send back with credential
    3. Server check if can participate in federate -> download if allowed
    4. Federate if download have enough stuff
    """

    def eligible_client(self, client_ptr):
        return client_ptr[:2] not in self.waiting_client

    def step_client(self, client_ptr, step=1):
        router = router_factory.get_default_router()
        addr, model_id, version = client_ptr
        self_model_download_credential = self.give_fetch_credential(client_ptr)
        self.waiting_client_lock.acquire()
        self.waiting_client[client_ptr[:2]] = self_model_download_credential[-2]  # self version within credential
        self.waiting_client_lock.release()
        router.send(addr, "cli_step__" + "s____",
                    ((model_id, self.uuid, self.version, step), self_model_download_credential))

    def step(self, args):
        if self.model_lock.locked():
            return False
        self.model_lock.acquire(), self.export_lock["i"].acquire(), self.export_lock["f"].acquire()
        num_step = args[0]  # first argument is number of step trained
        for i in range(num_step):
            self._step(args[1:])
        self.model_lock.release(), self.export_lock["i"].release(), self.export_lock["f"].release()
        return True

    def _step(self, args):
        import random
        random.seed()
        t = random.choice([2, 6, 10])
        time.sleep(t)
        self.dummy_content += self.uuid + " " + str(self.version) + " updated at " + str(time.ctime(time.time())) + "\n"
        self.version += 1

    def load_server(self, server_ptr):
        server_ptr = server_ptr[:2]
        self.dummy_content += "Load server: " + str(server_ptr) + "with credential " + str(
            self.get_server_model()[server_ptr]) + "\n"

    def ack_client_done(self, server_ptr):
        self.export_model()
        credential = self.give_fetch_credential(server_ptr)
        router = router_factory.get_default_router()
        addr, remote_server_id, remote_server_version = server_ptr
        router.send(addr, "cli_step__" + "a____", (remote_server_id, self.uuid, credential, self.cs_info))

    def eligible_federate(self, client_ptr, client_model_download_credential, mode="syn"):
        client_ptr = client_ptr[:2]
        model_not_expired = (mode == "syn" and client_model_download_credential[-1] == self.version) or (
                mode == "async")
        return client_ptr in self.waiting_client and model_not_expired

    def client_can_participate(self, client_ptr, mode="syn"):
        if mode == "asyn": return True
        if mode == "syn": return (client_ptr[:2] in self.client_model) and self.client_model[client_ptr[:2]][
            -1] == self.version

    def can_federate(self, mode="syn"):
        if mode == "asyn": return len(self.client_model) > 0
        if mode == "syn": return sum([cred[-1] == self.version for cred in
                                      self.get_client_model().values()]) >= self.synchronous_federate_minimum_client

    def load_client(self, client_ptr):
        client_ptr = client_ptr[:2]
        self.dummy_content += "Load client " + str(self.index_client(client_ptr)) + ": " + str(
            client_ptr) + "with credential " + str(self.get_client_model()[client_ptr]) + "\n"
        self.client_model_cache.append(client_ptr)

    def index_client(self, client_ptr):
        li = sorted([cli_ptr[:2] for cli_ptr in self.get_client()])
        return li.index(client_ptr[:2])

    def federate(self, mode="syn", federation_algo="none"):
        self.model_lock.acquire(), self.export_lock["i"].acquire(), self.export_lock["f"].acquire()
        self.dummy_content += self.uuid + " " + str(self.version) + " start_fl at " + str(
            time.ctime(time.time())) + "\n"
        if type(self.client_model_cache) is dict:
            for k in self.client_model_cache:
                self.client_model_cache[k].clear()
        if type(self.client_model_cache) is list: self.client_model_cache.clear()

        if self.can_federate(mode):
            for cli in self.get_client_model():
                if self.client_can_participate(cli, mode):
                    self.load_client(cli)

            self.federate_algo(federation_algo)
            self.export_lock["f"].release()
            self.version += 1
            self.export_model()
            self.model_lock.release()
            self.export_lock["i"].release()

    def federate_algo(self):
        self.dummy_content += "Federation federate " + str(len(self.client_model_cache)) + " clients.\n"

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
        dic = {"s": ignore_third(self.get_server()), "c": ignore_third(self.get_client()),
               "p": ignore_third(self.get_peer())}
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
        self.waiting_client_lock.acquire()
        self.waiting_client.pop(remote_ptr[:2], None)
        self.waiting_client_lock.release()

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
        if (server_addr, remote_model_id) not in self.get_remote_fetch_model_credential(role):
            return
        remote_file_name, username, password, ftp_addr, remote_version, self_version = \
            self.remote_fetch_model_credential[role][ptr]
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

    def add_client(self, client_addr, additional_args=None):
        router = router_factory.get_default_router()
        router.send(client_addr, "relation__as" + self._name, (self.uuid, self.version, additional_args))

    def add_server(self, server_addr, additional_args=None):
        router = router_factory.get_default_router()
        router.send(server_addr, "relation__ac" + self._name, (self.uuid, self.version, additional_args))

    def add_peer(self, peer_addr, additional_args=None):
        router = router_factory.get_default_router()
        router.send(peer_addr, "relation__ap" + self._name, (self.uuid, self.version, additional_args))

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
        self.client_performance_lock.acquire()
        self.client_performance[client_ptr[:2]] = {"data_size": 0, "train_one_time": 0, "epoch_time": 0,
                                                   "loading_time": 0, "transmission_time": 0}
        self.client_performance_lock.release()

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
