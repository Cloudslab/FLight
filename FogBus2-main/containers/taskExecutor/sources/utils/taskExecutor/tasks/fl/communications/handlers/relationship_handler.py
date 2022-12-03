"""Handler to handle relationships"""
from .abstract_handler import abstract_handler
from ...warehouse.warehouse import warehouse
from ...fl_apis.relationship_apis.model_pointer import model_pointer
import pickle
from enum import Enum


class relationship_handler(abstract_handler):
    name = "relat"

    class sub_events(Enum):
        add_client = 1
        add_server = 2
        add_peer = 3
        ack_add = 4

    def __call__(self, conn, reply_addr, *args, **kwargs):
        data_received = pickle.loads((conn.recv(2048)))
        sub_event = data_received["sub_event"]
        if sub_event == self.sub_events.add_server:
            model_name, reply_id, additional_args = data_received["model_name"], data_received["reply_uuid"], data_received["additional_args"]
            new_model = self._name_to_model[model_name](additional_args=additional_args)
            remote_ptr = model_pointer(reply_id, reply_addr)
            new_model.add_ptr("c", remote_ptr, additional_args)
            new_model.ack_add("s", remote_ptr, None)
        if sub_event == self.sub_events.add_client:
            model_name, reply_id, additional_args = data_received["model_name"], data_received["reply_uuid"], data_received["additional_args"]
            new_model = self._name_to_model[model_name](additional_args=additional_args)
            remote_ptr = model_pointer(reply_id, reply_addr)
            new_model.add_ptr("s", remote_ptr, additional_args)
            new_model.ack_add("c", remote_ptr, None)
        if sub_event == self.sub_events.add_peer:
            model_name, reply_id, additional_args = data_received["model_name"], data_received["reply_uuid"], data_received["additional_args"]
            new_model = self._name_to_model[model_name](additional_args=additional_args)
            remote_ptr = model_pointer(reply_id, reply_addr)
            new_model.add_ptr("p", remote_ptr, additional_args)
            new_model.ack_add("p", remote_ptr, None)
        if sub_event == self.sub_events.ack_add:

            reply_id, additional_args, local_id, role_of_remote = data_received["reply_uuid"], data_received["additional_args"], data_received["remote_uuid"], data_received["role_of_this_model"]
            model = warehouse().get_model(local_id)
            if model:
                model.add_ptr(role_of_remote, model_pointer(reply_id, reply_addr), additional_args)

    def __init__(self):
        self._name_to_model = {}
        self.import_models()

    def import_models(self):
        from ...fl_apis.base import base
        self._name_to_model[base.name] = base
