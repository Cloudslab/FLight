"""
Handles when ask to fetch data

1. handle of fetch data: push______:
    _c_s_ : client push server
    _s_c_ : server push client
"""
import pickle
from ..federaed_learning_model.datawarehouse import data_warehouse
from ..federaed_learning_model.linear_regression import linear_regression


class push_handler:

    def __call__(self, conn, addr, model_type, *args, **kwargs):

        data = pickle.loads(conn.recv(1024))
        remote_id, model_id, remote_model = data
        model = data_warehouse.get(model_id)
        if model_type == "_c_s_":
            if model and model.can_load("client", (remote_id, addr), remote_model[-2]):
                # ToDo: encapsulate this in model
                model.versions[(remote_id, addr)] = remote_model[-2]
                model.models[(remote_id, addr)] = remote_model
                if model.can_federate():
                    model.federate(lambda li : sum(li) / len(li))

        if model_type == "_s_c_":
            if model and model.can_load("server", (remote_id, addr), remote_model[-2]):
                model.load(remote_model)
                model.versions[(remote_id, addr)] = remote_model[-2]
                model.ack_ready("client", (addr, remote_id), "_fl_r")
