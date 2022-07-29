"""
Handles when ask to fetch data

1. handle of fetch data: push______:
    _c_s_ : client push server

"""
import pickle
from ..federaed_learning_model.datawarehouse import data_warehouse
from ..federaed_learning_model.linear_regression import linear_regression


class push_handler:

    def __call__(self, conn, addr, model_type, *args, **kwargs):
        if model_type == "_c_s_":
            data = pickle.loads(conn.recv(1024))
            remote_id, model_id, remote_model = data

            model = data_warehouse.get(model_id)
            if model and model.can_load("client", (remote_id, addr), remote_model[-2]):
                # ToDo: encapsulate this in model
                model.versions[(remote_id, addr)] = remote_model[-2]
                model.models[(remote_id, addr)] = remote_model
                if model.can_federate():
                    print("continue")
