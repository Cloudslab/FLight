import pickle
from ..federaed_learning_model.datawarehouse import model_warehouse
from ..federaed_learning_model.base import base_model


class model_communication_handler:
    def __call__(self, conn, addr, sub_event, *args, **kwargs):
        if sub_event[0] == "f": # fetch
            remote_id, self_version, local_model_id, remote_version = pickle.loads(conn.recv(2048))
            model = model_warehouse().get(local_model_id)
            ptr = addr, remote_id, remote_version
            if model and model.can_fetch(ptr, sub_event[1]):
                credential = model.give_fetch_credential(ptr)
                remote_role_to_self_role = {"s": "c", "c": "s", "p": "p"}
                model.send_download_credential(ptr, remote_role_to_self_role[sub_event[1]], credential)
            else:
                pass

        if sub_event[0] == "p": # handle push
            remote_id, local_model_id, credential = pickle.loads(conn.recv(2048))
            model = model_warehouse().get(local_model_id)
            ptr = addr, remote_id, None
            if model and model.remote_credential_valid(ptr, sub_event[1], credential):
                model.save_download_model_credential(ptr, sub_event[1], credential)