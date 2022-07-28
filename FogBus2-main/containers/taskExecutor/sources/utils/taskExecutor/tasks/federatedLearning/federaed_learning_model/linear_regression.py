"""
w: weight
b: bias
lr: learning rate
version: model version
uuid: model id
"""
from .base_model import base_model
from ..communicate.router import router_factory
from .datawarehouse import data_warehouse
import pickle


class linear_regression(base_model):

    def __init__(self, w, b, lr, uuid = None):
        self.w = w
        self.b = b
        self.lr = lr
        self.version = 1
        self.client = {}
        self.server = {}
        self.peer = {}
        self.waiting_list = {}
        self.uuid = data_warehouse.set(self)

    def ack_ready(self, role, ptr):
        pass

    def add_peer(self, ptr):
        pass

    def add_server(self, ptr):
        pass

    def ask_next(self, role, ptr):
        pass

    def can_federate(self):
        return True

    def can_fetch(self, role, ptr):
        return True

    def can_load(self, role, ptr):
        return True

    def federate(self, fl_algo):
        pass

    def fetch_client(self, client_id):
        pass

    def fetch_peer(self, peer_id):
        pass

    def fetch_server(self, server_id):
        pass

    # ------------------------ pass all line ------------------------------

    def step(self, train_data):
        # for large ds, train_data can be necessary information to load dataset
        x, y = train_data

        def grad(x_ele, y_ele):
            l = self.w * x_ele + self.b - y_ele
            return l, l * x_ele

        def grad_all(x_list, y_list):
            if len(x_list) != len(y_list) or len(x_list) == 0:
                # should be an error here
                return None

            grad_B, grad_W = 0, 0
            for x_ele, y_ele in zip(x_list, y_list):
                grad_b, grad_w = grad(x_ele, y_ele)
                grad_B += grad_b
                grad_W += grad_w

            return grad_B / len(x_list), grad_W / len(x_list)

        grad_B, grad_W = grad_all(x, y)

        self.b = self.b - self.lr * grad_B
        self.w = self.w - self.lr * grad_W
        self.version += 1

    def load(self, data):
        data = pickle.loads(data)
        if len(data) == 3:
            self.w, self.b, self.lr = data
        elif len(data) == 2:
            self.w, self.b = data
        self.version += 1

    def export(self):
        return pickle.dumps((self.w, self.b, self.lr, self.version, self.uuid))

    def add_client(self, addr):
        router = router_factory.get_default_router()
        router.send(addr, "register", self.export())

if __name__ == "__main__":
    pass