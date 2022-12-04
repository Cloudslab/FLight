"""Stores weights of remote model """
from threading import Lock
from datetime import datetime


class cache_manager:
    def __init__(self):
        self._cache = {
            "general": [],
            "client_models": [],
            "server_models": [],
            "peer_models": [],
            "federated_results": None
        }
        self._cache_lock = {
            "general": Lock(),
            "client_models": Lock(),
            "server_models": Lock(),
            "peer_models": Lock(),
            "federated_results": Lock()
        }

    def save_to_cache(self, model_in_dict, access_to_cache="general"):
        if access_to_cache not in ["client_models", "server_models", "peer_models", "general"]:
            return
        self._cache_lock[access_to_cache].acquire()
        self._cache[access_to_cache].append(model_in_dict)
        self._cache_lock[access_to_cache].release()

    def can_federate(self, required_response=None, required_time=None, additional_args=None):
        response_enough = not required_response or len(self._cache[required_response[0]]) >= required_response[1]
        time_out = not required_time or datetime.now().timestamp() > (required_time[0] + required_time[1])
        return response_enough and time_out
