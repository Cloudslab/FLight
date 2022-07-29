"""
Handles when receive an confirm called ack_ready______

1. handle of add client federated learning: ack_ready__fl__

"""
import pickle
from ..federaed_learning_model.datawarehouse import data_warehouse
from ..federaed_learning_model.linear_regression import linear_regression


class ack_ready_handler:

    def __call__(self, conn, addr, model_type, *args, **kwargs):
        data = pickle.loads(conn.recv(1024))
        role, (model_id, remote_id) = data
        model = data_warehouse.get(model_id)
        if model_type == "_fl_r": # _fl_r is the flag of ack register is ready/ ready to train
            if model:
                if role == "client":
                    if (remote_id, addr) not in model.client:
                        model.client.append((remote_id, addr))
                    model.ready_to_train_client += 1
                elif role == "server":
                    model.server.append((remote_id, addr))
                elif role == "peer":
                    model.peer.append((remote_id, addr))

        if model_type == "_fl_t": # _fl_t is the flag of ack train is done, can be fetched
            if model:
                if role == "client" and (remote_id, addr) in model.client: # ToDo: add more fetch condition
                    model.fetch_client((addr, remote_id))

        if model_type == "_fl_f": # _fl_f is the flag of server get updated, can be fetched
            if model:
                if role == "server" and (remote_id, addr) in model.server: # ToDo: add more fetch condition
                    model.fetch_server((addr, remote_id))
