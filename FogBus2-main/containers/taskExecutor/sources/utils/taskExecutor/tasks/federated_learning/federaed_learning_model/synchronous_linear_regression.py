from .base import base_model
import torch
import time
import pickle
import random
from torch.autograd import Variable


class linear_regression(base_model):
    def __init__(self, default_xy_generator_param=None, database_credential=None):
        super().__init__(export_at_creation=False)
        self._name = "lrs"
        self.lr = LinearRegressionModel()
        self.x_data = None
        self.y_data = None
        self.synchronous_federate_minimum_client = 3
        if default_xy_generator_param:
            w, b = default_xy_generator_param
            self.x_data = Variable(torch.Tensor([[i] for i in range(10)]))
            self.y_data = Variable(torch.Tensor([[w*i+b] for i in range(10)])) # since here is no scaling, can support up to y = 10x + 10
        self.database_credential = database_credential
        self.export_model()

    def _step(self, args):
        x_data, y_data = None, None
        if self.database_credential:
            pass
        else:
            x_data, y_data = self.x_data, self.y_data
        self.dummy_content += self.uuid + " " + str(self.version) + " updated at " + str(time.ctime(time.time())) + "\n"
        self.lr.step(x_data, y_data, 1)
        self.version += 1

    def _export_model(self, export_file_path):
        f = open(export_file_path, "wb+")
        binary_self = self.lr.linear.__dict__["_parameters"]["weight"].data, self.lr.linear.__dict__["_parameters"]["bias"].data
        f.write(pickle.dumps(binary_self))
        f.close()

    def load_server(self, server_ptr):
        self.model_lock.acquire(), self.export_lock["i"].acquire(), self.export_lock["f"].acquire()
        server_model_path, _, _ = self.get_server_model()[server_ptr[:2]]
        f = open(server_model_path, "rb")
        self.lr.linear.__dict__["_parameters"]["weight"].data, self.lr.linear.__dict__["_parameters"]["bias"].data = pickle.loads(f.read())
        f.close()
        self.model_lock.release(), self.export_lock["i"].release(), self.export_lock["f"].release()

    def load_client(self, client_ptr):
        client_path, _, _ = self.get_client_model()[client_ptr[:2]]
        f = open(client_path, "rb")
        self.client_model_cache.append(pickle.loads(f.read())) # weight data & bias data
        f.close()
        self.dummy_content += "Load client " + str(self.index_client(client_ptr)) + ": " + str(
            client_ptr) + "with credential " + str(self.get_client_model()[client_ptr]) + "\n"

    def federate_algo(self):
        w = [ele[0] for ele in self.client_model_cache]
        b = [ele[1] for ele in self.client_model_cache]
        self.lr.linear.weight.data = sum(w)/len(w)
        self.lr.linear.bias.data = sum(b)/len(w)


class LinearRegressionModel(torch.nn.Module):

    def __init__(self):
        super(LinearRegressionModel, self).__init__()
        self.linear = torch.nn.Linear(1, 1)  # One in and one out
        self.criterion = torch.nn.MSELoss(size_average=False)
        self.optimizer = torch.optim.SGD(self.parameters(), lr=0.001)

    def forward(self, x):
        y_pred = self.linear(x)
        return y_pred

    def step(self, x_data=None, y_data=None, num_iter=1):
        for i in range(num_iter):
            pred_y = self(x_data)
            loss = self.criterion(y_data, pred_y)
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
            # print('epoch {}, loss {}'.format(i, loss.item()))
