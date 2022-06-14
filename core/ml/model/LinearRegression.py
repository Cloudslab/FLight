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
        self.w = w
        self.b = b
        self.lr = lr
        self.version = 1
        self.ptr = ptr

    # for worker side it is a normal training loop
    # for server side it is an aggregation

    def step(self, x, y):
        def grad(x_ele, y_ele):
            l = self.w.value * x_ele - y_ele
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


class LinearRegressionServer(LinearRegression):
    def __init__(self, w, b, lr, ptr):
        super().__init__(w, b, lr, ptr)
        self.worker_ptrs = list()
        self.w_list = list()
        self.b_list = list()

    def request_worker(self, client_address: Address):
        self.ptr.export_pointer(client_address)

    def add_worker_pointer(self, ptr_dict: dict):
        ptr = LinearRegressionPointer.fromDict(ptr_dict)
        self.add_worker_pointer(ptr)

    def add_worker_pointer(self, ptr: LinearRegressionPointer):
        # ToDo: check for repeated client/ format check
        self.worker_ptrs.append(ptr)

    def fetch(self):
        pass

    def step(self):
        pass
