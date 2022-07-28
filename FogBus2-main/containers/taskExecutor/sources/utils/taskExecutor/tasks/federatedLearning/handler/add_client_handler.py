"""
Handles when receive an event called add_client______

1. handle of add client federated learning: add_client_fl__

"""
import pickle
from ..federaed_learning_model.datawarehouse import data_warehouse
from ..federaed_learning_model.linear_regression import linear_regression

class add_client_handler:

    def __call__(self, conn, addr, model_type, *args, **kwargs):
        if model_type == "_fl__":
            data = pickle.loads(conn.recv(1024))
            w, b, lr, version, uuid = data
            model = linear_regression(w, b, lr)
            model.server.append(uuid)
            model.ack_ready("client", 123)
            print(model.uuid)
            print(model.server[0])
