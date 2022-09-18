from abc import ABC, abstractmethod


class base_model_abstract(ABC):

    @abstractmethod
    def export(self):
        pass

    """
    Functions to transmit model
    """

    @abstractmethod
    def fetch_server(self, server_model_ptr):
        pass
    
    @abstractmethod
    def fetch_client(self, client_model_ptr):
        pass
    
    @abstractmethod
    def fetch_peer(self, peer_model_ptr):
        pass

    @abstractmethod
    def can_fetch(self, remote_ptr, role):
        pass

    @abstractmethod
    def give_fetch_credential(self, remote_ptr, mode="f"):
        pass

    @abstractmethod
    def _export_model(self, export_file_path):
        pass

    @abstractmethod
    def export_model(self, mode="f", file_extension=".txt"):
        pass

    @abstractmethod
    def send_download_credential(self, remote_ptr, role, credential):
        pass

    @abstractmethod
    def save_download_model_credential(self, remote_ptr, role, credential):
        pass

    @abstractmethod
    def remote_credential_valid(self, remote_ptr, role, credential):
        pass

    @abstractmethod
    def download_model(self, remote_ptr, role, local_destination=None):
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
