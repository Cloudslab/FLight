"""Manages remote model weights (those haven't downloaded to local sites)"""
from ..relationship_apis.model_pointer import model_pointer


class remote_model_weights_manager:
    def __init__(self):
        self.remote_model_weights = {}  # {model_ptr: (remote_version, based_on_which_local_version, other info)}

    def update_weights_info(self, remote_ptr: model_pointer, remote_version, base_local_version, download_credentials=None, additional_args=None):
        record = self.remote_model_weights.get(remote_ptr, (-1, -1, None))
        if record[0] < remote_version:
            self.remote_model_weights[remote_ptr] = (remote_version, base_local_version, download_credentials, additional_args)

    def get_available_remote_model_weights(self):
        return self.remote_model_weights
