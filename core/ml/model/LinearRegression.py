"""
A simple linear regression: y = wx + b

"""

from ...communication.utils.types import Address
from .LinearRegressionPointer import LinearRegressionPointer
from .Model import Model
from ..basic.Scalar import Scalar
from ...warehouse.DataWarehouse import DataWarehouse
from ...warehouse.ModelWarehouse import ModelRetriever

# ToDo: factor out factory class
class LinearRegressionFactory:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(LinearRegressionFactory, cls).__new__(cls)
        return cls.instance

    @classmethod
    def LinearRegressionServer(cls, w_init, b_init, lr, address: Address):
        # Initialize server side linear regression together with the pointer
        model = LinearRegressionServer(w_init, b_init, lr, None)
        uuid = DataWarehouse().set(ModelRetriever.RETRIEVER_NAMESPACE, model)
        model.ptr = LinearRegressionPointer(model, address, uuid)

        return model

    @classmethod
    def LinearRegressionClient(cls, ptr: 'Pointer', address: Address):
        # Initialize client side linear regression based on a pointer from server
        if isinstance(ptr, dict):
            ptr = LinearRegressionPointer.fromDict(ptr)

        model = LinearRegressionClient(None, None, None, None, ptr)
        uuid = DataWarehouse().set(ModelRetriever.RETRIEVER_NAMESPACE, model)
        model.ptr = LinearRegressionPointer(model, address, uuid)

        return model


class LinearRegression(Model):
    def __init__(self, w: Scalar, b: Scalar, lr, ptr: LinearRegressionPointer):
        if not isinstance(w, Scalar):
            w = Scalar(w)
        if not isinstance(b, Scalar):
            b = Scalar(b)

        self.w = w
        self.b = b
        self.lr = lr
        self.version = 1
        self.ptr = ptr

    # for worker side it is a normal training loop
    # for server side it is an aggregation

    def step(self, x, y):
        def grad(x_ele, y_ele):
            l = self.w.value * x_ele + self.b.value - y_ele
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
        new_b, new_w = self.b.value - self.lr * grad_B, self.w.value - self.lr * grad_W
        self.b.update(new_b)
        self.w.update(new_w)
        self.version += 1

    # return all necessary data for this model
    def export(self):
        return self.b.value, self.w.value, self.lr

    # given weights from other, load to the model
    def load(self, b, w, lr):
        self.b.update(b)
        self.w.update(w)
        self.lr = lr
        self.version += 1


class LinearRegressionClient(LinearRegression):
    def __init__(self, w, b, lr, ptr, server_ptr: LinearRegressionPointer):
        super().__init__(w, b, lr, ptr)
        self.server_ptr = server_ptr

    # when server ask the client to do next round, client can choose to agree or reject
    # note if pointer for model hold on client side is newer than server side, reject (model out dated)
    def available(self, server_ptr_dict):
        # ToDo: check against local logic
        return self.server_ptr.address == server_ptr_dict["address"] and \
               self.server_ptr.remote_id == server_ptr_dict["remote_id"] and \
               self.server_ptr.version <= server_ptr_dict["version"]

    def fetch_server(self):
        self.server_ptr.fetch_server(self.ptr)

    # note if local server version is greater than the version send, then no need to load it
    def load_server(self, server_ptr_dict, data_dict):
        if self.available(server_ptr_dict):
            b, w, lr = data_dict["b"], data_dict["w"], data_dict["lr"]
            self.b.update(b)
            self.w.update(w)
            self.lr = lr
            self.server_ptr.version = server_ptr_dict["version"]

    def stepN(self, x, y, n=100, auto_push=True):
        for i in range(n):
            self.step(x, y)
        self.version += 1
        self.ptr.version += 1
        if auto_push:
            self.push_server()

    def push_server(self):
        b, w, lr = self.export()
        data = {"b": b, "w": w, "lr": lr}
        self.server_ptr.push_server(self.ptr, data, "train")

class LinearRegressionServer(LinearRegression):
    def __init__(self, w, b, lr, ptr):
        super().__init__(w, b, lr, ptr)
        self.worker_ptrs = list()
        self.w_list = list()
        self.b_list = list()
        self.waiting_next_round = 0

    def request_worker(self, client_address: Address):
        self.ptr.export_pointer(client_address)

    def add_worker_pointer(self, ptr: LinearRegressionPointer):
        # ToDo: check for repeated client/ format check
        # ToDo: package format check to another function
        if isinstance(ptr, dict):
            ptr = LinearRegressionPointer.fromDict(ptr)
        self.worker_ptrs.append(ptr)

    # notify all client on hold to start a new round training
    def notify_all(self):
        for ptr in self.worker_ptrs:
            ptr.step(self.ptr)

    # push data(model weights) to client for a train
    def push_all_client_train(self):
        b, w, lr = self.export()
        data = {"b": b, "w": w, "lr": lr}
        for cli_ptr in self.worker_ptrs:
            cli_ptr.push_client(self.ptr, data, "train")

    # check if available for a new fetch/ based on fetch from client
    def available_data(self, server_ptr_dict):
        return self.ptr.address == server_ptr_dict["address"] and \
               self.ptr.remote_id == server_ptr_dict["remote_id"] and \
               self.ptr.version >= server_ptr_dict["version"]

    # update client
    def update_client(self, client_ptr_dict, client_data):
        for clr in self.worker_ptrs:
            if clr.remote_id == client_ptr_dict["remote_id"] and clr.version < client_ptr_dict["version"]:
                clr.version = client_ptr_dict["version"]
                self.b_list.append(client_data["b"])
                self.w_list.append(client_data["w"])

    # do a federated learning, ToDo: l
    def fl_step(self, fl_algorithm):
        self.b.update(fl_algorithm(self.b_list))
        self.w.update(fl_algorithm(self.w_list))

    # clean up and move forward
    def next(self):
        self.w_list = list()
        self.b_list = list()
        self.waiting_next_round = 0
        self.ptr.version += 1
        self.version += 1
    # collect all client manually
    def fetch_all(self):
        pass
