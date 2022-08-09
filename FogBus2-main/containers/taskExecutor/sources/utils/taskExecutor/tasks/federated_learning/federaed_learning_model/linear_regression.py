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

    def __init__(self, w, b, lr):
        self.w = w
        self.b = b
        self.lr = lr
        self.version = 1
        self.client = []
        self.server = []
        self.peer = []
        self.uuid = data_warehouse.set(self)
        self.ready_to_train_client = 0
        self.versions = {}  # version
        self.models = {}  # remote models' local copy

    def add_peer(self, ptr):
        pass

    def add_server(self, ptr):
        pass

    def fetch_peer(self, ptr):
        pass

    def push_peer(self, ptr):
        pass

    # ------------------------ pass all line ------------------------------

    def load_data(self, info=None):
        if info:
            pass
        else:
            return data_warehouse.get_default_data()

    def step(self, train_data=None):
        # for large ds, train_data can be necessary information to load dataset
        if not train_data:
            train_data = self.load_data()
            if not train_data:
                return

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
        # data = pickle.loads(data)
        if len(data) >= 3:
            self.w, self.b, self.lr = data[:3]
        elif len(data) == 2:
            self.w, self.b = data
        self.version += 1

    def export(self):
        return self.w, self.b, self.lr, self.version, self.uuid

    def add_client(self, addr):
        ## ToDo: change addr to ptr: (addr, remote_id). Allow remote_id to be None
        router = router_factory.get_default_router()
        router.send(addr, "add_client_lr__", self.export())

    def ack_ready(self, role, ptr, flg):
        router = router_factory.get_default_router()
        addr, remote_id = ptr
        router.send(addr, "ack_ready_" + flg, (role, (remote_id, self.uuid)))

    def ask_next(self, itr_nums):
        router = router_factory.get_default_router()
        for (remote_id, addr) in self.client:
            router.send(addr, "ask_next___fl__", (self.uuid, remote_id, itr_nums))

    def can_next(self, ptr):
        return ptr in self.server

    def fetch_client(self, ptr):
        router = router_factory.get_default_router()
        addr, remote_id = ptr
        router.send(addr, "fetch______s_c_", (self.uuid, remote_id))

    def fetch_server(self, ptr):
        router = router_factory.get_default_router()
        addr, remote_id = ptr
        router.send(addr, "fetch______c_s_", (self.uuid, remote_id))

    def can_fetch(self, role, ptr):
        if role == "server" and ptr in self.server: return True
        if role == "client" and ptr in self.client: return True
        return False

    def push_server(self, ptr):
        router = router_factory.get_default_router()
        addr, remote_id = ptr
        router.send(addr, "push_______c_s_", (self.uuid, remote_id, self.export()))

    def push_client(self, ptr):
        router = router_factory.get_default_router()
        addr, remote_id = ptr
        router.send(addr, "push_______s_c_", (self.uuid, remote_id, self.export()))

    def can_load(self, role, ptr, version):
        remote_id, addr = ptr
        if role == "client" and ptr in self.client and (
                remote_id not in self.versions or self.versions[remote_id] < version): return True
        if role == "server" and ptr in self.server and (
                remote_id not in self.versions or self.versions[remote_id] < version): return True

        return False

    # change this function to achieve synchronous/ asynchronous federated
    # if can_federate always true, then it is asynchronous
    def can_federate(self):
        return len(self.models) >= 3

    # ToDo: currently there is only linear regression + fed_average, can factor this part out when have more federated
    # algorithm comming in
    def federate(self, fl_algo):
        W, B = [], []
        for w_, b_, _, _, _ in self.models.values():
            W.append(w_)
            B.append(b_)
            self.ready_to_train_client -= 1

        self.w = fl_algo(W)
        self.b = fl_algo(B)
        self.version += 1
        self.models.clear()

        for remote_id, addr in self.client:
            self.ack_ready("server", (addr, remote_id), "_fl_f")


if __name__ == "__main__":
    pass
