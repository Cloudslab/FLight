"""Handle communication of model weights between different parties"""
from ..training_apis.ml_models.ml_model import ml_model
from ..relationship_apis.model_pointer import model_pointer
from .fetcher import fetcher

class model_transmission_manager:
    def __init__(self):
        self._fetcher = fetcher()

    def generate_access(self, remote_ptr: model_pointer, model_object: ml_model):
        pass

    def export_model(self, model_object: ml_model):
        pass

    def load_model_to_cache(self, cache: dict, cache_type):
        pass

    def fetch_remote(self, self_uuid, remote_ptr: model_pointer, additional_args=None):
        return self._fetcher.fetch_remote(self_uuid, remote_ptr, additional_args)

    def download_model(self, local_file_path, credentials):
        pass

