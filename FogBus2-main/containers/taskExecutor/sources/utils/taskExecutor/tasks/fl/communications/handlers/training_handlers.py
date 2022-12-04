"""Handlers to handle request about trainings"""


from .abstract_handler import abstract_handler
from ...warehouse.warehouse import warehouse
from ...fl_apis.relationship_apis.model_pointer import model_pointer
import pickle
from enum import Enum


class training_handler(abstract_handler):
    name = "train"

    class sub_events(Enum):
        train_remote = 1
        ack_train_finish = 2

    def __call__(self, conn, reply_addr, *args, **kwargs):
        data_received = pickle.loads((conn.recv(2048)))
        sub_event = data_received["sub_event"]

        if sub_event == self.sub_events.train_remote:
            steps, additional_args, reply_uuid, local_uuid, evaluate, credential = \
                data_received["steps"], \
                data_received["additional_args"], \
                data_received["reply_uuid"], \
                data_received["remote_uuid"], \
                data_received["evaluate"], \
                data_received["credential"]
            remote_ptr = model_pointer(reply_uuid, reply_addr)
            model = warehouse().get_model(local_uuid)
            if model:  # can add criteria here to check if eligible to request train
                # get model on server before starts to train
                id_of_local_cache = model.download_model(credential["credential"])
                model.load_model_dict(warehouse().get_model(id_of_local_cache))
                model.train(steps, additional_args, evaluate)
                model.ack_train_finish(remote_ptr)

        if sub_event == self.sub_events.ack_train_finish:
            local_uuid, reply_uuid, base_version, remote_version = \
                data_received["remote_uuid"], \
                data_received["reply_uuid"], \
                data_received["base_version"], \
                data_received["self_version"]

            model = warehouse().get_model(local_uuid)
            if model:
                remote_ptr = model_pointer(reply_uuid, reply_addr)
                model.update_weights_info(remote_ptr, remote_version, base_version)

