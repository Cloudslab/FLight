"""
Handles when receive an event called add_client______

1. handle of add client federated learning: add_client_lr__

"""
import pickle
from ..federaed_learning_model.datawarehouse import data_warehouse
from ..federaed_learning_model.linear_regression import linear_regression

class add_client_handler:

    def __call__(self, conn, addr, model_type, *args, **kwargs):
        if model_type == "_lr__":
            data = pickle.loads(conn.recv(1024))
            w, b, lr, version, uuid = data
            model = linear_regression(w, b, lr)
            model.server.append((uuid, addr))
            model.ack_ready("client", (addr, model.server[0][0]))
