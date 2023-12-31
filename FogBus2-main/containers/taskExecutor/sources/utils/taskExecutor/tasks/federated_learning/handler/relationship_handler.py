import pickle
from ..federaed_learning_model.datawarehouse import model_warehouse
from ..federaed_learning_model.base import base_model
from ..federaed_learning_model.synchronous_linear_regression import linear_regression
from ..federaed_learning_model.synchronous_cv import synchronous_computer_vision
from ..federaed_learning_model.minst import minst_classification
from ..federaed_learning_model.cifar10 import cifar10_classification

model_handbook = {
    "bas": base_model,
    "lrs": linear_regression,
    "cv1": synchronous_computer_vision,
    "mst": minst_classification,
    "cif": cifar10_classification
}


class relationship_handler:
    def __call__(self, conn, addr, sub_event, *args, **kwargs):
        if sub_event[0] == "a":  # add a relationship
            model = model_handbook[sub_event[2:]]
            remote_id, remote_version, additional_args = pickle.loads(conn.recv(1024))
            if additional_args: model = model(additional_args)
            else: model = model()
            ptr = addr, remote_id, remote_version
            model.add_ptr(ptr, sub_event[1])  # add as server, add as client or add as peer
            remote_role_to_self_role = {"s": "c", "c": "s", "p": "p"}
            model.ack_add(ptr, remote_role_to_self_role[sub_event[1]])

        if sub_event[0] == "c":  # handle remote confirm a relationship
            remote_id, remote_version, local_model_id, additional_args = pickle.loads(conn.recv(4096))
            model = model_warehouse().get(local_model_id)
            ptr = addr, remote_id, remote_version, additional_args
            if model and model.can_add(ptr, sub_event[1]):
                if sub_event[1] != 'c':
                    ptr = ptr[:3]
                model.add_ptr(ptr, sub_event[1])
