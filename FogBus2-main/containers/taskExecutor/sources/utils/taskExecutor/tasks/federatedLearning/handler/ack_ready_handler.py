"""
Handles when receive an confirm called ack_ready______

1. handle of add client federated learning: ack_ready__fl__

"""
import pickle
from ..federaed_learning_model.datawarehouse import data_warehouse
from ..federaed_learning_model.linear_regression import linear_regression


class ack_ready_handler:

    def __call__(self, conn, addr, model_type, *args, **kwargs):
        if model_type == "_fl_r":
            data = pickle.loads(conn.recv(1024))
            role, (model_id, remote_id) = data
            model = data_warehouse.get(model_id)
            if model:
                if role == "client":
                    model.client.append((remote_id, addr))
                elif role == "server":
                    model.server.append((remote_id, addr))
                elif role == "peer":
                    model.peer.append((remote_id, addr))
