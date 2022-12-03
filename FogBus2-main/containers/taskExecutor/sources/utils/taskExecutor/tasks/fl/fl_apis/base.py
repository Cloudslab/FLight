"""Base model class, wraps APIS of subcomponents"""

from .relationship_apis.relationship_manager import relationship_manager
from .training_apis.training_apis import ml_train_apis
from ..warehouse.warehouse import warehouse
from .training_apis.ml_models.dummy_model import dummy_model

class base:

    name = "base"
    underlying_model = dummy_model

    def __init__(self, other_init_args=None, ml_model_initialise_args=None, additional_args=None):
        self._relationship_handler = relationship_manager()
        self._ml_train_apis = ml_train_apis(base.underlying_model, ml_model_initialise_args, additional_args)
        self.uuid = warehouse().set_model(self)

        # expose relationship APIS here
        self.add_client = lambda client_address, additional_args=None: self._relationship_handler.add_client(client_address, self.uuid, self.name, additional_args)
        self.add_server = lambda server_address, additional_args=None: self._relationship_handler.add_server(server_address, self.uuid, self.name, additional_args)
        self.add_peer = lambda peer_address, additional_args=None: self._relationship_handler.add_peer(peer_address, self.uuid, self.name, additional_args)
        self.add_ptr = lambda role_of_remote, remote_ptr, additional_args=None: self._relationship_handler.add_ptr(role_of_remote, remote_ptr, additional_args)
        self.ack_add = lambda role_of_this_model, remote_ptr, additional_args=None: self._relationship_handler.ack_add(self.uuid, role_of_this_model, remote_ptr, additional_args)
        self.get_clients = self._relationship_handler.get_clients
        self.get_servers = self._relationship_handler.get_servers
        self.get_peers = self._relationship_handler.get_peers

        # expose training APIS here
        self.train = self._ml_train_apis.train
        self.train_remote = lambda steps, remote_ptr, additional_args=None, evaluate=False: self._ml_train_apis.train_remote(self.uuid, steps, remote_ptr, additional_args, evaluate)
        self.ack_train_finish = lambda remote_ptr: self._ml_train_apis.ack_train_finish(self.uuid, remote_ptr)
        self.federate = self._ml_train_apis.federate
        self.can_federate = self._ml_train_apis.can_federate
        self.get_model_dict = self._ml_train_apis.get_model_dict
        self.update_weights_info = self._ml_train_apis.update_weights_info
        self.get_available_remote_model_weights = self._ml_train_apis.get_available_remote_model_weights
