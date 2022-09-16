import pickle
from ..federaed_learning_model.datawarehouse import model_warehouse
from ..federaed_learning_model.base import base_model

class rpc_handler:
    def __call__(self, conn, addr, sub_event, *args, **kwargs):
        (remote_id, remote_version, local_model_id, remote_rpc_string, call_back_rpc_string, args), role = pickle.loads(conn.recv(4096)), sub_event[0]
        ptr = addr, remote_id, remote_version
        model = model_warehouse().get(local_model_id)
        if model: model.run_rpc(ptr, role, remote_rpc_string, call_back_rpc_string, args)
