"""Handles requests about sending model weights from one site to another"""


from .abstract_handler import abstract_handler
from ...warehouse.warehouse import warehouse
from ...fl_apis.relationship_apis.model_pointer import model_pointer
import pickle
from enum import Enum


class model_communication_handler(abstract_handler):
    name = "comut"

    class sub_event(Enum):
        fetch_model_weights = 1
        provide_credential = 2

    def __call__(self, conn, reply_addr, *args, **kwargs):
        data_received = pickle.loads((conn.recv(2048)))
        sub_event = data_received["sub_event"]
        if sub_event == self.sub_event.fetch_model_weights:
            local_uuid, reply_uuid, additional_args = data_received["remote_uuid"], data_received["reply_uuid"], data_received["additional_args"]
            model = warehouse().get_model(local_uuid)
            if model:  # add access check here
                remote_ptr = model_pointer(reply_uuid, reply_addr)
                model.provide_access(remote_ptr, additional_args)

        if sub_event == self.sub_event.provide_credential:
            credential, reply_uuid, local_uuid, additional_args = data_received["credential"], data_received["reply_uuid"], data_received["remote_uuid"], data_received["additional_args"]
            model = warehouse().get_model(local_uuid)
            if model:  # can check if still interested
                id_of_local_cache = model.download_model(credential)
                model.save_to_cache(warehouse().get_model(id_of_local_cache))
