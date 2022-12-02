"""Base model class"""

from relationship_apis.relationship_manager import relationship_manager
from ..warehouse.warehouse import warehouse


class base:
    def __init__(self):
        self._relationship_handler = relationship_manager()
        self.uuid = warehouse().set_model(self)

        # expose relationship APIS handlers here
        self.add_client = lambda client_address, additional_args: self._relationship_handler.add_client(
            client_address, self.uuid, additional_args)
        self.add_server = lambda server_address, additional_args: self._relationship_handler.add_server(
            server_address, self.uuid, additional_args)
        self.add_peer = lambda peer_address, additional_args: self._relationship_handler.add_peer(
            peer_address, self.uuid, additional_args)
        self.ack_add = self._relationship_handler.ack_add
        self.get_clients = self._relationship_handler.get_clients
        self.get_servers = self._relationship_handler.get_servers
        self.get_peers = self._relationship_handler.get_peers
