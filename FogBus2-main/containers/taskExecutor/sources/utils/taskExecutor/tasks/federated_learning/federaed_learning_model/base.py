from .base_model_abstract import base_model_abstract
from .datawarehouse import model_warehouse
from ..communicate.router import router_factory

class base_model(base_model_abstract):

    def __init__(self):
        self._name = "bas"
        self.uuid = model_warehouse().set(self)
        self.version = 1
        self.client = []
        self.client_waiting_list = []
        self.server = []
        self.server_waiting_list = []
        self.peer = []
        self.peer_waiting_list = []

    def export(self):
        return self.__dict__

    """
    Functions to handle relationships
    1. add_client/add_server/add_peer
    2. can_add(remote_ptr)
    3. ack_add(remote_ptr)
    4. _add_client/_add_server/_add_peer
    """

    def add_client(self, remote_addr):
        router = router_factory.get_default_router()
        router.send(remote_addr, "relation__as"+self._name, (self.uuid, self.version))

    def add_server(self, server_addr):
        pass

    def add_peer(self, peer_addr):
        pass

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
        pass

    def _add_server(self, server_ptr):
        self.server.append(server_ptr)

    def _add_peer(self, peer_ptr):
        pass

    def ack_add(self, remote_ptr):
        router = router_factory.get_default_router()
        addr, model_id, version = remote_ptr
        router.send(addr, "relation__cc___", (self.uuid, self.version, model_id))


