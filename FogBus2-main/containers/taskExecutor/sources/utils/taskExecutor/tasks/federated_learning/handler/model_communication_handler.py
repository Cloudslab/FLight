import pickle
from ..federaed_learning_model.datawarehouse import model_warehouse
from ..federaed_learning_model.base import base_model


class model_communication_handler:
    def __call__(self, conn, addr, sub_event, *args, **kwargs):
        if sub_event[0] == "f": # fetch
            remote_id, self_version, local_model_id, remote_destination = pickle.loads(conn.recv(2048))
            model = model_warehouse().get(local_model_id)
            if model and model.can_fetch((addr, remote_id), sub_event[1]):
                remote_role_to_self_role = {"s": "c", "c": "s", "p": "p"}
                response_type, fetch_credential = model.export_model()
                role = remote_role_to_self_role[sub_event[1]]
                ptr = addr, remote_id, None
                model.push_model(ptr, role, (response_type, fetch_credential), remote_destination)
            else:
                pass

        if sub_event[0] == "p": # handle push
            remote_id, remote_version, local_model_id, local_destination, data = pickle.loads(conn.recv(2048))
            model = model_warehouse().get(local_model_id)
            ptr = addr, remote_id, remote_version
            if model and model.can_import(sub_event[1], data, local_destination, ptr):
                model.import_model(sub_event[1], data, local_destination, ptr)
                model.fetch_model(sub_event[1], None, ptr)