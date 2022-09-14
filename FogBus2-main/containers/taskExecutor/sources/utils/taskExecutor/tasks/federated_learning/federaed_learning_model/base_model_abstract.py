from abc import ABC, abstractmethod


class base_model_abstract(ABC):

    @abstractmethod
    def export(self):
        pass

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


    @abstractmethod
    def fetch_server(self, server_model_ptr):
        pass
    
    @abstractmethod
    def fetch_client(self, client_model_ptr):
        pass
    
    @abstractmethod
    def fetch_peer(self, peer_model_ptr):
        pass

    """
    @abstractmethod
    def can_fetch(self, remote_ptr, role):
        pass
    
    @abstractmethod
    def export_model(self, destination):
        pass
    
    @abstractmethod
    def push_model(self, client_ptr, t, data, remote_dest):
        pass
    
    @abstractmethod
    def import_model(self, t, data, dest):
        pass
    """


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
