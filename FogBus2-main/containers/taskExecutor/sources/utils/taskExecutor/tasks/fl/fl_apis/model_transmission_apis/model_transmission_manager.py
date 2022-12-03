"""Handle communication of model weights between different parties"""
from ..training_apis.ml_models.ml_model import ml_model
from ..relationship_apis.model_pointer import model_pointer


class model_transmission_manager:
    def __init__(self):
        pass

    def generate_access(self, remote_ptr: model_pointer, model_object: ml_model):
        pass

    def export_model(self, model_object: ml_model):
        pass

    def load_model_to_cache(self, cache: dict, cache_type):
        pass

    def fetch_remote(self, remote_ptr: model_pointer):
        pass

    def download_model(self, local_file_path, credentials):
        pass

