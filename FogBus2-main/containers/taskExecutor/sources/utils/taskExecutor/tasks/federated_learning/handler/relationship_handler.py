import pickle
from ..federaed_learning_model.datawarehouse import model_warehouse
from ..federaed_learning_model.base import base_model

model_handbook = {
    "bas": base_model
}
class relationship_handler:
    def __call__(self, conn, addr, sub_event, *args, **kwargs):
        if sub_event[0] == "a": # add a relationship
            model = model_handbook[sub_event[0:]]()
            remote_id, remote_version = pickle.loads(conn.recv(1024))
            ptr = addr, remote_id, remote_version
            model.add_ptr(ptr, sub_event[1]) # add as server, add as client or add as peer
            model.ack_add(ptr)

        if sub_event[0] == "c": # handle remote confirm a relationship
            remote_id, remote_version, local_model_id = pickle.loads(conn.recv(1024))
            model = model_warehouse().get(local_model_id)
            ptr = addr, remote_id, remote_version
            if model & model.can_add(ptr, sub_event[1]):
                model.add_ptr(ptr, sub_event[1])

