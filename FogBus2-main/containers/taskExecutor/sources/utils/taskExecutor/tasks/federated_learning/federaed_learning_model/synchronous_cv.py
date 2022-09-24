from .base import base_model
import time
import pickle
import random

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.autograd import Variable
from .datawarehouse import data_warehouse

class synchronous_computer_vision(base_model):
    def __init__(self, train_file_idx=0):
        super().__init__(export_at_creation=False)
        self._name = "cv1"
        self.cv1 = Net()
        self.train_data = data_warehouse.get_cv1_data(train_file_idx)
        self.test_data = data_warehouse.get_cv1_data(role="test")
        self.synchronous_federate_minimum_client = 3
        self.export_model()
        self.accuracy = 0
        self.client_model_cache = {
            "conv1_w":[],
            "conv1_b":[],
            "conv2_w":[],
            "conv2_b":[],
            "fc_w":[],
            "fc_b":[],
            "accuracy":[]
        }

    def _export_model(self, export_file_path):
        f = open(export_file_path, "wb+")
        binary_self = {
            "conv1_w": self.cv1.conv1.weight.data,
            "conv1_b": self.cv1.conv1.bias.data,
            "conv2_w": self.cv1.conv2.weight.data,
            "conv2_b": self.cv1.conv2.bias.data,
            "fc_w": self.cv1.fc.weight.data,
            "fc_b": self.cv1.fc.bias.data,
            "accuracy": self.cv1.accuracy
        }
        f.write(pickle.dumps(binary_self))
        f.close()

    def load_server(self, server_ptr):
        self.model_lock.acquire(), self.export_lock["i"].acquire(), self.export_lock["f"].acquire()
        server_model_path, _, _ = self.get_server_model()[server_ptr[:2]]
        f = open(server_model_path, "rb")
        param_dict = pickle.loads(f.read())
        f.close()
        self.cv1.conv1.weight.data = param_dict["conv1_w"]
        self.cv1.conv1.bias.data = param_dict["conv1_b"]
        self.cv1.conv2.weight.data = param_dict["conv2_w"]
        self.cv1.conv2.bias.data = param_dict["conv2_b"]
        self.cv1.fc.weight.data = param_dict["fc_w"]
        self.cv1.fc.bias.data = param_dict["fc_b"]

        self.model_lock.release(), self.export_lock["i"].release(), self.export_lock["f"].release()

    def _step(self, args):
        self.dummy_content += self.uuid + " " + str(self.version) + " updated at " + str(time.ctime(time.time())) + "\n"
        # train model
        self.cv1.step(self.train_data)
        # calculate accuracy
        self.cv1.test(self.test_data)
        self.version += 1
        time.sleep(1)

    def stepp(self, args):
        self.dummy_content += self.uuid + " " + str(self.version) + " updated at " + str(time.ctime(time.time())) + "\n"
        # train model
        self.cv1.step(self.train_data)
        # calculate accuracy
        self.cv1.test(self.test_data)
        self.version += 1
        time.sleep(1)

    def load_client(self, client_ptr):
        client_path, _, _ = self.get_client_model()[client_ptr[:2]]
        f = open(client_path, "rb")
        dict_client = pickle.loads(f.read()) # weight data & bias data
        f.close()
        for key in dict_client:
            self.client_model_cache[key].append(dict_client[key])
        # write log
        self.dummy_content += "Load client " + str(self.index_client(client_ptr)) + ": " + str(
            client_ptr) + "with credential " + str(self.get_client_model()[client_ptr]) + "\n"

    def federate_algo(self):
        l_client = len(self.client_model_cache["conv1_w"])
        self.cv1.conv1.weight.data = sum(self.client_model_cache["conv1_w"])/l_client
        self.cv1.conv1.bias.data = sum(self.client_model_cache["conv1_b"])/l_client
        self.cv1.conv2.weight.data = sum(self.client_model_cache["conv2_w"])/l_client
        self.cv1.conv2.bias.data = sum(self.client_model_cache["conv2_b"])/l_client
        self.cv1.fc.weight.data = sum(self.client_model_cache["fc_w"])/l_client
        self.cv1.fc.bias.data = sum(self.client_model_cache["fc_b"])/l_client
        self.cv1.accuracy = sum(self.client_model_cache["accuracy"])/l_client

        self.dummy_content += "Achieve average accuracy of " + str(self.cv1.accuracy) + "\n"

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
        self.mp = nn.MaxPool2d(2)
        self.fc = nn.Linear(320, 10)
        self.optimizer = optim.SGD(self.parameters(), lr=0.01, momentum=0.5)
        self.accuracy = 0

    def forward(self, x):
        # in_size = 64
        in_size = x.size(0) # one batch
        # x: 64*10*12*12
        x = F.relu(self.mp(self.conv1(x)))
        # x: 64*20*4*4
        x = F.relu(self.mp(self.conv2(x)))
        # x: 64*320
        x = x.view(in_size, -1) # flatten the tensor
        # x: 64*10
        x = self.fc(x)
        return F.log_softmax(x)

    def step(self, ds):
        for data, target in ds:
            self.optimizer.zero_grad()
            output = self(data)
            loss = F.nll_loss(output, target)
            loss.backward()
            self.optimizer.step()

    def test(self, test_data):
        total_ele = 0
        correct = 0
        for data, target in test_data:
            total_ele += len(target)
            output = self(data)
            pred = output.data.max(1, keepdim=True)[1]
            correct += pred.eq(target.data.view_as(pred)).cpu().sum()
        self.accuracy = correct/total_ele * 100