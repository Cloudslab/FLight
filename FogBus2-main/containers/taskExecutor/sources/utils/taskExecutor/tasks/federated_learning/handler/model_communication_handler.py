import pickle
from ..federaed_learning_model.datawarehouse import model_warehouse
from ..federaed_learning_model.base import base_model


class model_communication_handler:
    def __call__(self, conn, addr, sub_event, *args, **kwargs):
        if sub_event[0] == "f": # fetch
            remote_id, self_version, local_model_id, destination = pickle.loads(conn.recv(2048))
            model = model_warehouse().get(local_model_id)
            if model:
                x = 1
                x.sot()
            else:
                y = 1
                y.sot()