"""Handle communication of model weights between different parties"""
from ..training_apis.ml_models.ml_model import ml_model
from ..relationship_apis.model_pointer import model_pointer
from ...communications.router import router
from ...communications.handlers.model_communication_handlers import model_communication_handler

class model_transmission_manager:
    def __init__(self):
        pass

    def generate_access(self, remote_ptr: model_pointer, model_object: ml_model):
        pass

    def export_model(self, model_object: ml_model):
        pass

    def load_model_to_cache(self, cache: dict, cache_type):
        pass

    @staticmethod
    def fetch_remote(self_uuid, remote_ptr: model_pointer, additional_args=None):
        r = router.get_default_router()
        r.send(remote_ptr.address, model_communication_handler.name, {
            "sub_event": model_communication_handler.sub_event.fetch_model_weights,
            "reply_uuid": self_uuid,
            "remote_uuid": remote_ptr.uuid,
            "additional_args": additional_args
        })

    def download_model(self, local_file_path, credentials):
        pass

