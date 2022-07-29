"""
Handles when ask to train next

1. handle of add client federated learning: ack_next___fl__

"""
import pickle
from ..federaed_learning_model.datawarehouse import data_warehouse
from ..federaed_learning_model.linear_regression import linear_regression


class ack_next_handler:

    def __call__(self, conn, addr, model_type, *args, **kwargs):
        if model_type == "_fl__":
            data = pickle.loads(conn.recv(1024))
            remote_id, model_id, itr_nums = data
            model = data_warehouse.get(model_id)
            if model and model.can_next((remote_id, addr)):
                for i in range(itr_nums):
                    model.step()
