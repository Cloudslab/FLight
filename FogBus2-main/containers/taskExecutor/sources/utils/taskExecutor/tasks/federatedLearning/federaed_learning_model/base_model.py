"""
base_model defines common behavior all model involved within federated learning should behave.

1. step(): a train epoch of current model
2. federate(fl_algo): perform a federated learning based on a federated algorithm
3. fetch_server(server_id): ask weights from server
4. fetch_client(ptr): ask weights from client
5. fetch_peer(peer_id): request weights from peer
6. export(): export weights
7. load(data): load weights
8. can_fetch(role, ptr): check if another model can access weights of this model
9. can_load(role, ptr): check if another model contribute weights of this model
10. add_server/client/peer(ptr): request a model to be aggregation server/client/peer and take current model as worker:
    if ptr contain both address & model local id, then request the model
    if ptr only contain address, then request a new model on address side
11. can_federate(): condition for next federation:
    always true:
        - asynchronous fl
    need all/ proportion of client update
        - synchronous fl
12. ack_ready(role, ptr):
    tell other this model finish update
13. ask_next(role, ptr):
    ask others to perform next round operation(typically server ask worker to perform operation)
14. can_next(ptr):
    ask whether a remote model can ask local train

"""
from abc import ABC, abstractmethod


class base_model(ABC):

    @abstractmethod
    def step(self, train_data):
        raise NotImplementedError("Override with a epoch of train of this model")

    @abstractmethod
    def federate(self, fl_algo):
        raise NotImplementedError("Override with a federate child logic")

    @abstractmethod
    def fetch_server(self, server_id):
        raise NotImplementedError("Override with logic of sending request to fetch server model")

    @abstractmethod
    def fetch_client(self, ptr):
        raise NotImplementedError("Override with logic of fetching child model based on child ptr")

    @abstractmethod
    def fetch_peer(self, peer_id):
        raise NotImplementedError("Override with logic of fetching peer model based on peer id")

    @abstractmethod
    def export(self):
        raise NotImplementedError("Override with logic of export weights to a serializable data type")

    @abstractmethod
    def load(self, data):
        raise NotImplementedError("Override with logic of import weights to current model")

    @abstractmethod
    def can_fetch(self, role, ptr):
        raise NotImplementedError("Override with logic checking if others can fetch weights of the model")

    @abstractmethod
    def can_load(self, role, ptr):
        raise NotImplementedError("Override with logic checking if others can load(contribute) this model.")

    @abstractmethod
    def add_server(self, ptr):
        raise NotImplementedError("Override with logic of requesting a federated learning relationship with server.")

    @abstractmethod
    def add_client(self, addr):
        raise NotImplementedError("Override with logic of requesting a federated learning relationship with client.")

    @abstractmethod
    def add_peer(self, ptr):
        raise NotImplementedError("Override with logic of requesting a federated learning relationship with peer.")

    @abstractmethod
    def can_federate(self):
        raise NotImplementedError("Override with logic of whether can perform another federated learning.")

    @abstractmethod
    def ack_ready(self, role, ptr, flg):
        raise NotImplementedError("Override with logic of ack model is ready to another model with connection")

    @abstractmethod
    def ask_next(self, itr_nums):
        raise NotImplementedError("Override with logic of asking a remote model to do training")

    @abstractmethod
    def can_next(self, ptr):
        raise NotImplementedError("Override with logic of whether a remote model can ask local train")

