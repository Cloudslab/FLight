"""Handle communication of model weights between different parties"""
from ..training_apis.ml_models.ml_model import ml_model
from ..relationship_apis.model_pointer import model_pointer
from ...communications.handlers.model_communication_handlers import model_communication_handler
from ...communications.router import router
from threading import Lock
from ...warehouse.warehouse import warehouse


class model_transmission_manager:
    def __init__(self):
        self._version_to_id = {}  # (model_version:int, model_id:str)
        self._max_version = -1
        self._export_lock = Lock()

    def generate_access(self, model_object: ml_model, model_uuid, additional_args=None):
        self.export_model(model_object, model_uuid)
        v_current = self._max_version
        credential = warehouse().get_model(self._version_to_id[v_current])
        return {"credential": credential,
                "reply_uuid": model_uuid,
                "additional_args": additional_args,
                "version": v_current}

    def provide_access(self, remote_ptr: model_pointer, model_object: ml_model, model_uuid, additional_args=None):
        response = self.generate_access(model_object, model_uuid, additional_args)
        response["sub_event"] = model_communication_handler.sub_event.provide_credential
        response["remote_uuid"] = remote_ptr.uuid
        r = router.get_default_router()
        r.send(remote_ptr.address, model_communication_handler.name, response)

    def export_model(self, model_object: ml_model, model_uuid, extension=".txt"):
        self._export_lock.acquire()
        if self._max_version >= model_object.version:
            self._export_lock.release()
            return
        model_version, model_dict = model_object.version, model_object.to_dict()
        file_name = "".join([model_uuid, "_", str(model_version), extension])
        model_id = warehouse().set_model({"raw_data": model_dict, "file_name": file_name}, storage="ftp")
        self._version_to_id[model_version] = model_id
        self._max_version = model_version
        self._export_lock.release()

    @staticmethod
    def fetch_remote(self_uuid, remote_ptr: model_pointer, additional_args=None):
        r = router.get_default_router()
        r.send(remote_ptr.address, model_communication_handler.name, {
            "sub_event": model_communication_handler.sub_event.fetch_model_weights,
            "reply_uuid": self_uuid,
            "remote_uuid": remote_ptr.uuid,
            "additional_args": additional_args
        })

    @staticmethod
    def download_model(credentials):
        ftp_address, user_name, password, file_path = credentials
        local_model_id = warehouse().download_model(ftp_address, file_path, user_name, password)
        return local_model_id
