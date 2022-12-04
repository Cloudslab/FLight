"""
Functions define behaviors related to federated model training


1. the model trains locally: train(self, steps, additional_args)
2. request remote model to train: train_remote(self, steps, remote_ptr, additional_args)
3. federate received response: federate(access_to_cache, federated_algo)
4. whether a federated learning can proceed or not: can_federate(self, required_response=None, required_time=None, additional_args=None)
"""

from threading import Lock
from datetime import datetime
from ...communications.router import router
from ..relationship_apis.model_pointer import model_pointer
from ...communications.handlers.training_handlers import training_handler


class ml_train_apis:
    def __init__(self, model_class, ml_model_initialise_args=None, additional_args=None):
        self._model = model_class(ml_model_initialise_args)
        self._model_lock = Lock()


        # expose model's common apis
        self.get_model_dict = self._model.to_dict
        self.get_model_object = lambda: self._model
        self.load_model_dict = self._model.from_dict

    def train(self, steps, additional_args=None, evaluate=False):
        self._model_lock.acquire()
        for i in range(steps):
            self._model.train(additional_args)
        if evaluate:
            self._model.evaluate()
        self._model_lock.release()

    @staticmethod
    def train_remote(self_uuid, steps, remote_ptr: model_pointer, additional_args=None, evaluate=False,
                     model_download_credentials=None):
        r = router.get_default_router()
        r.send(remote_ptr.address, training_handler.name, {
            "sub_event": training_handler.sub_events.train_remote,
            "steps": steps,
            "additional_args": additional_args,
            "reply_uuid": self_uuid,
            "remote_uuid": remote_ptr.uuid,
            "evaluate": evaluate,
            "credential": model_download_credentials
        })

    def ack_train_finish(self, self_uuid, remote_ptr: model_pointer, base_version, model_download_credential=None):
        r = router.get_default_router()
        r.send(remote_ptr.address, training_handler.name, {
            "sub_event": training_handler.sub_events.ack_train_finish,
            "reply_uuid": self_uuid,
            "remote_uuid": remote_ptr.uuid,
            "base_version": base_version,
            "self_version": self._model.version,
            "credential": model_download_credential
        })

    # def federate(self, access_to_cache, federated_algo):
    #    if access_to_cache not in ["client_models", "server_models", "peer_models"]:
    #        return
    #    self._cache_lock[access_to_cache].acquire()
    #    temp = self._cache[access_to_cache].copy()
    #    self._cache_lock[access_to_cache].release()
    #    res = federated_algo(temp)
    #    self._cache_lock["federated_results"].acquire()
    #    self._cache["federated_results"] = res
    #    self._cache_lock["federated_results"].release()

    # required_response : (type, count), e.g.("peer_models", 5)
    # required_time: (time_stamp, duration), e.g.(12345.3212, 20)
