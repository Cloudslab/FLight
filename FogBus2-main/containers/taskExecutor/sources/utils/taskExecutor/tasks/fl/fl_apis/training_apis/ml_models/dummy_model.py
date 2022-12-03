"""Sample Implementation for test purpose"""

from .ml_model import ml_model
from threading import Lock

class dummy_model(ml_model):
    def __init__(self, additional_args=None):
        super(dummy_model, self).__init__(additional_args)
        self._model_lock = Lock()
        self.content = ""
        self.count = 0

    def train(self, additional_args=None):
        self.content += "Dummy train " + str(self.count) + "\n"
        self.count += 1
        super(dummy_model, self).train(additional_args)

    def evaluate(self):
        self.content += "Dummy evaluate " + str(self.count) + "\n"
        self.count += 1

    def to_dict(self):
        self._model_lock.acquire()
        res = {"count": self.count}
        self._model_lock.release()
        return res

    def from_dict(self, dict_model: dict):
        self._model_lock.acquire()
        self.count = dict_model["count"]
        self._model_lock.release()
