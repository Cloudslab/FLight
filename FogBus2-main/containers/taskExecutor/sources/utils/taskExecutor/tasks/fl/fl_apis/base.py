"""Base model class, wraps APIS of subcomponents"""

from .relationship_apis.relationship_manager import relationship_manager
from ..warehouse.warehouse import warehouse


class base:

    name = "base"

    def __init__(self, additional_init_args=None):
        self._relationship_handler = relationship_manager()
        self.uuid = warehouse().set_model(self)

        # expose relationship APIS here
        self.add_client = lambda client_address, additional_args=None: self._relationship_handler.add_client(
            client_address, self.uuid, self.name, additional_args)
        self.add_server = lambda server_address, additional_args=None: self._relationship_handler.add_server(
            server_address, self.uuid, self.name, additional_args)
        self.add_peer = lambda peer_address, additional_args=None: self._relationship_handler.add_peer(
            peer_address, self.uuid, self.name, additional_args)
        self.add_ptr = lambda role_of_remote, remote_ptr, additional_args=None: self._relationship_handler.add_ptr(
            role_of_remote, remote_ptr, additional_args)
        self.ack_add = lambda role_of_this_model, remote_ptr, additional_args=None: self._relationship_handler.ack_add(
            self.uuid, role_of_this_model, remote_ptr, additional_args)
        self.get_clients = self._relationship_handler.get_clients
        self.get_servers = self._relationship_handler.get_servers
        self.get_peers = self._relationship_handler.get_peers
