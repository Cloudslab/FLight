from abc import ABC, abstractmethod


class base_model_abstract(ABC):

    @abstractmethod
    def export(self):
        pass

    """
    Functions to handle relationships
    1. add_client/add_server/add_peer
    2. can_add(remote_ptr)
    3. ack_add(remote_ptr)
    4. _add_client/_add_server/_add_peer
    """
    @abstractmethod
    def add_client(self, client_addr):
        pass

    @abstractmethod
    def add_server(self, server_addr):
        pass

    @abstractmethod
    def add_peer(self, peer_addr):
        pass

    @abstractmethod
    def can_add(self, remote_ptr, role):
        pass

    @abstractmethod
    def add_ptr(self, remote_ptr, role):
        pass

    @abstractmethod
    def _add_client(self, client_ptr):
        pass

    @abstractmethod
    def _add_server(self, server_ptr):
        pass

    @abstractmethod
    def _add_peer(self, peer_ptr):
        pass

    @abstractmethod
    def ack_add(self, remote_ptr, role):
        pass
