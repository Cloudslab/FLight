"""Base model class, wraps APIS of subcomponents"""

from .relationship_apis.relationship_manager import relationship_manager
from .training_apis.training_apis import ml_train_apis
from ..warehouse.warehouse import warehouse
from .model_transmission_apis.model_transmission_manager import model_transmission_manager
from .training_apis.ml_models.dummy_model import dummy_model
from .cache_apis.cache_manager import cache_manager
from .remote_model_weights_apis.remote_model_weights_manager import remote_model_weights_manager
from .training_apis.fl_algorithms.federated_average import federated_average

class base:

    name = "base"
    underlying_model = dummy_model
    average_algorithm = federated_average().federate

    def __init__(self, other_init_args=None, ml_model_initialise_args=None, additional_args=None):
        self._relationship_handler = relationship_manager()
        self._ml_train_apis = ml_train_apis(base.underlying_model, ml_model_initialise_args, additional_args)
        self._model_transmission_manager = model_transmission_manager()
        self._cache_manager = cache_manager()
        self._remote_model_weights_manager = remote_model_weights_manager()

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
        self.train_remote = lambda steps, remote_ptr, additional_args=None, evaluate=False, additional_args_for_access=None: self._ml_train_apis.train_remote(self.uuid, steps, remote_ptr, additional_args, evaluate, self.generate_access(additional_args_for_access))
        self.ack_train_finish = lambda remote_ptr, base_version, additional_args_for_access=None: self._ml_train_apis.ack_train_finish(self.uuid, remote_ptr, base_version, self.generate_access(additional_args_for_access))
        self.get_model_dict = self._ml_train_apis.get_model_dict
        self.load_model_dict = self._ml_train_apis.load_model_dict
        self.federate = lambda federated_algo=base.average_algorithm, additional_args=None, access_to_cache="general": self._ml_train_apis.federate(self._cache_manager.clear_cache(access_to_cache), federated_algo, additional_args)

        # expose model transmission APIs here
        self.fetch_remote = lambda remote_ptr, additional_args=None: self._model_transmission_manager.fetch_remote(self.uuid, remote_ptr, additional_args)
        self.generate_access = lambda additional_args=None: self._model_transmission_manager.generate_access(self._ml_train_apis.get_model_object(), self.uuid, additional_args)
        self.provide_access = lambda remote_ptr, additional_args=None: self._model_transmission_manager.provide_access(remote_ptr, self._ml_train_apis.get_model_object(), self.uuid, additional_args)
        self.download_model = self._model_transmission_manager.download_model

        # expose cache (remote model weights stored locally) management apis here
        self.save_to_cache = self._cache_manager.save_to_cache
        self.can_federate = self._cache_manager.can_federate
        self.clear_cache = self._cache_manager.clear_cache

        # expose model cache related APIs here
        self.update_weights_info = self._remote_model_weights_manager.update_weights_info
        self.get_available_remote_model_weights = self._remote_model_weights_manager.get_available_remote_model_weights
        self.get_available_remote_model_weight_credential = self._remote_model_weights_manager.get_available_remote_model_weight_credential
