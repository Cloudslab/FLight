"""
Manages relationships between nodes
"""

import threading
from .model_pointer import model_pointer
from ...communications.router import router
from ...communications.handlers.relationship_handler import relationship_handler


class relationship_manager:
    def __init__(self):
        self.clients = []
        self.servers = []
        self.peers = []
        self.clients_lock = threading.Lock()
        self.servers_lock = threading.Lock()
        self.peers_lock = threading.Lock()

    def get_clients(self):
        return self.clients.copy()

    def get_servers(self):
        return self.servers.copy()

    def get_peers(self):
        return self.peers.copy()

    @staticmethod
    def add_client(client_address, self_uuid, additional_args=None):
        r = router.get_default_router()
        r.send(client_address, relationship_handler.name,
               {"sub_event": relationship_handler.sub_events.add_client,
                "reply_uuid": self_uuid,
                "additional_args": additional_args})

    @staticmethod
    def add_server(server_address, self_uuid, additional_args=None):
        r = router.get_default_router()
        r.send(server_address, relationship_handler.name,
               {"sub_event": relationship_handler.sub_events.add_server,
                "reply_uuid": self_uuid,
                "additional_args": additional_args})

    @staticmethod
    def add_peer(server_address, self_uuid, additional_args=None):
        r = router.get_default_router()
        r.send(server_address, relationship_handler.name,
               {"sub_event": relationship_handler.sub_events.add_peer,
                "reply_uuid": self_uuid,
                "additional_args": additional_args})

    def _add_client(self, client_ptr: model_pointer, additional_args=None):
        self.clients_lock.acquire()
        if client_ptr not in self.clients:
            self.clients.append(client_ptr)
        self.clients_lock.release()

    def _add_server(self, server_ptr: model_pointer, additional_args=None):
        self.servers_lock.acquire()
        if server_ptr not in self.servers:
            self.servers.append(server_ptr)
        self.servers_lock.release()

    def _add_peer(self, peer_ptr: model_pointer, additional_args=None):
        self.peers_lock.acquire()
        if peer_ptr not in self.peers:
            self.peers.append(peer_ptr)
        self.servers_lock.release()

    def add_ptr(self, role_of_remote, remote_ptr: model_pointer, additional_args=None):
        if role_of_remote == "c" and remote_ptr not in self.clients:
            self._add_client(remote_ptr, additional_args)
        if role_of_remote == "s" and remote_ptr not in self.servers:
            self._add_server(remote_ptr, additional_args)
        if role_of_remote == "p" and remote_ptr not in self.peers:
            self._add_server(remote_ptr, additional_args)

    @staticmethod
    def ack_add(self_uuid, role_of_this_model, remote_ptr: model_pointer, additional_args=None):
        r = router.get_default_router()
        r.send(remote_ptr.address, relationship_handler.name,
               {"sub_event": relationship_handler.sub_events.ack_add,
                "reply_uuid": self_uuid,
                "role_of_this_model": role_of_this_model,
                "additional_args": additional_args})
