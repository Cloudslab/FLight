"""
Handles when ask to fetch data

1. handle of fetch data: fetch_____:
    _s_c_ : server fetch client
    _c_s_ : client fetch server

"""
import pickle
from ..federaed_learning_model.datawarehouse import data_warehouse
from ..federaed_learning_model.linear_regression import linear_regression


class fetch_handler:

    def __call__(self, conn, addr, model_type, *args, **kwargs):
        if model_type == "_s_c_":
            data = pickle.loads(conn.recv(1024))
            remote_id, model_id = data
            model = data_warehouse.get(model_id)
            if model and model.can_fetch("server", (remote_id, addr)):
                model.push_server((addr, remote_id))

        if model_type == "_c_s_":
            data = pickle.loads(conn.recv(1024))
            remote_id, model_id = data
            model = data_warehouse.get(model_id)
            if model and model.can_fetch("client", (remote_id, addr)):
                model.push_client((addr, remote_id))
