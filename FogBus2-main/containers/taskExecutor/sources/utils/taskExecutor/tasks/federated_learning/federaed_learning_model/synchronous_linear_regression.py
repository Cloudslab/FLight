from .base import base_model
import torch
import time
import pickle
import random
from torch.autograd import Variable
from .datawarehouse import data_warehouse


class linear_regression(base_model):
    def __init__(self, learning_rate=0.05):
        super().__init__(export_at_creation=False)
        self._name = "lrs"
        self.lr = LinearRegressionModel(learning_rate)
        self.synchronous_federate_minimum_client = 3
        self.export_model()

    def _step(self, args):
        x_data, y_data = self.load_data()
        self.dummy_content += self.uuid + " " + str(self.version) + " updated at " + str(time.ctime(time.time())) + "\n"
        self.lr.step(x_data, y_data, 1)
        self.version += 1

    def _export_model(self, export_file_path):
        f = open(export_file_path, "wb+")
        binary_self = self.lr.bias, self.lr.weight, self.lr.train_len
        f.write(pickle.dumps(binary_self))
        f.close()

    def load_server(self, server_ptr):
        self.model_lock.acquire(), self.export_lock["i"].acquire(), self.export_lock["f"].acquire()
        server_model_path, _, _ = self.get_server_model()[server_ptr[:2]]
        f = open(server_model_path, "rb")
        self.lr.bias, self.lr.weight, _ = pickle.loads(f.read())
        f.close()
        self.model_lock.release(), self.export_lock["i"].release(), self.export_lock["f"].release()

    def load_client(self, client_ptr):
        client_path, _, _ = self.get_client_model()[client_ptr[:2]]
        f = open(client_path, "rb")
        self.client_model_cache.append(pickle.loads(f.read())) # weight data & bias data
        f.close()
        self.dummy_content += "Load client " + str(self.index_client(client_ptr)) + ": " + str(
            client_ptr) + "with credential " + str(self.get_client_model()[client_ptr]) + "\n"

    def federate_algo(self, algo):
        w = [ele[1] for ele in self.client_model_cache]
        b = [ele[0] for ele in self.client_model_cache]
        n = [ele[2] for ele in self.client_model_cache]
        if sum(n) == 0:
            return
        ww = [ni/sum(n) for ni in n]
        self.lr.weight = sum([a*b for a, b in zip(w,ww)])
        self.lr.bias = sum([a*b for a, b in zip(b,ww)])

    def load_data(self, info=None):

        if info:
            pass
        else:
            xy = data_warehouse.read_from_database("xy")
            X = []
            Y = []
            for _, x, y in xy:
                X.append(x)
                Y.append(y)
            return X, Y

class LinearRegressionModel():

    def __init__(self, learning_rate=0.05):
        self.learning_rate = learning_rate
        self.weight = 0
        self.bias = 0
        self.train_len = 0

    def step(self, x_data=None, y_data=None, num_iter=1):
        if len(x_data) < 2:
            self.train_len = 0
            return

        sumx = sum(x_data)
        sumy = sum(y_data)
        sumx2 = sum([x*x for x in x_data])
        sumy2 = sum([y * y for y in y_data])
        sumxy = sum([x*y for x,y in zip(x_data,y_data)])
        n = len(x_data)

        beta0 = (sumy * sumx2 - sumx * sumxy) / (n * sumx2 - sumx * sumx)
        beta1 = (n * sumxy - sumx * sumy) / (n * sumx2 - sumx*sumx)
        grad_bias = (beta0 - self.bias) * self.learning_rate
        grad_weig = (beta1 - self.weight) * self.learning_rate

        for i in range(num_iter):
            self.bias += grad_bias
            self.weight += grad_weig

        self.train_len = n

