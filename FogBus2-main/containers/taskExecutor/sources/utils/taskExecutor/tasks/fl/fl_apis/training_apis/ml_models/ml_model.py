"""Defines functions of ML training"""


class ml_model:

    def train(self, additional_args=None):
        self.version += 1

    def evaluate(self):
        pass

    def to_dict(self):
        pass

    def from_dict(self, model_dict: dict):
        pass

    def __init__(self, additional_args=None):
        self.version = 0
