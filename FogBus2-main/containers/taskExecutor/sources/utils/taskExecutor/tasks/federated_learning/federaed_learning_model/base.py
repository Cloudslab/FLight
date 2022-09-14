from .base_model_abstract import base_model_abstract
from .datawarehouse import model_warehouse
from ..communicate.router import router_factory


class base_model(base_model_abstract):

    def __init__(self):
        self._name = "bas"
        self.uuid = model_warehouse().set(self)
        self.version = 1
        self.client = []
        self._client_waiting_list = []
        self.server = []
        self._server_waiting_list = []
        self.peer = []
        self._peer_waiting_list = []

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

    def export(self):
        return self.__dict__

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
        self.client.append(client_ptr)

    def _add_server(self, server_ptr):
        self.server.append(server_ptr)

    def _add_peer(self, peer_ptr):
        self.peer.append(peer_ptr)

    def ack_add(self, remote_ptr, role):
        router = router_factory.get_default_router()
        addr, model_id, version = remote_ptr
        router.send(addr, "relation__c" + role + "___", (self.uuid, self.version, model_id))

    """
    END-----------------------------------------------------------------------------------
    """
