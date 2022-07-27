"""
w: weight
b: bias
lr: learning rate
version: model version
uuid: model id
"""
from base_model import base_model


class linear_regression(base_model):

    def __init__(self, w, b, lr, uuid):
        self.w = w
        self.b = b
        self.lr = lr
        self.version = 1
        self.uuid = uuid

    def step(self, train_data):
        #for large ds, train_data can be necessary information to load dataset



