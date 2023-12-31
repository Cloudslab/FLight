import pickle
from ..federaed_learning_model.datawarehouse import model_warehouse
from ..federaed_learning_model.base import base_model
import time

class remote_call_handler:
    def __call__(self, conn, addr, sub_event, *args, **kwargs):
        if sub_event[0] == "s": # step command from server
            (local_model_id, remote_model_id, remote_model_version, step), credential = pickle.loads(conn.recv(4096))
            ptr = addr, remote_model_id, remote_model_version
            model = model_warehouse().get(local_model_id)
            if model and model.remote_credential_valid(ptr, "s", credential):
                model.save_download_model_credential(ptr, "s", credential)
                model.download_model(ptr, "s")
                model.load_server(ptr)
                if model.step((step,)):
                    model.ack_client_done(ptr)

        if sub_event[0] == "a": # ack client ready
            local_model_id, remote_model_id, credential, performance = pickle.loads(conn.recv(4096))
            ptr = addr, remote_model_id, credential[-2] # credential[-2] is remote model version
            model = model_warehouse().get(local_model_id)
            if model and model.eligible_federate(ptr, credential):
                model.save_download_model_credential(ptr, "c", credential)
                download_start_time = time.time()
                model.download_model(ptr, "c")
                download_end_time = time.time()
                model.update_client_performance(ptr, performance)
                model.update_client_performance(ptr, {"transmission_time": download_end_time - download_start_time+1})
            else:
                # only save the credential
                model.save_download_model_credential(ptr, "c", credential)