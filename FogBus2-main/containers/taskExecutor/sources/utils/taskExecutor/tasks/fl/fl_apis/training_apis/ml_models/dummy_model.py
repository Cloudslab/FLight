"""Sample Implementation for test purpose"""

from .ml_model import ml_model


class dummy_model(ml_model):
    def __init__(self, additional_args=None):
        super(dummy_model, self).__init__(additional_args)
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
        return {"count": self.count}

    def from_dict(self, dict_model: dict):
        self.count = dict_model["count"]

