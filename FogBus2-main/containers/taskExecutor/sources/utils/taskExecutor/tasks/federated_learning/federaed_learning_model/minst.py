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
import math

REST_TIME = 0.5

class minst_classification(base_model):
    def __init__(self, args=(0, 1)):
        super().__init__(export_at_creation=False)
        self._name = "mst"
        self.model = CNN()
        self.test_data, self.train_data = data_warehouse.get_MINST_data(args[0], args[1])
        self.cs_info["data_size"] = len(self.train_data)
        self.min_client = 10
        self.server_version = -1
        self.export_model()
        self.client_model_cache = {
            "conv1_w": [],
            "conv1_b": [],
            "conv2_w": [],
            "conv2_b": [],
            "fc_w": [],
            "fc_b": [],
            "data_size": [],
            "server_version": []
        }

    def _export_model(self, export_file_path):
        f = open(export_file_path, "wb+")
        binary_self = {
            "conv1_w": self.model.conv1[0].weight.data,
            "conv1_b": self.model.conv1[0].bias.data,
            "conv2_w": self.model.conv2[0].weight.data,
            "conv2_b": self.model.conv2[0].bias.data,
            "fc_w": self.model.out.weight.data,
            "fc_b": self.model.out.bias.data,
            "data_size": len(self.train_data),
            "server_version": self.server_version
        }
        f.write(pickle.dumps(binary_self))
        f.close()

    def load_server(self, server_ptr):
        load_time_start = time.time()
        self.model_lock.acquire(), self.export_lock["i"].acquire(), self.export_lock["f"].acquire()
        server_model_path, _, _ = self.get_server_model()[server_ptr[:2]]
        f = open(server_model_path, "rb")
        param_dict = pickle.loads(f.read())
        f.close()
        self.model.conv1[0].weight.data = param_dict["conv1_w"]
        self.model.conv1[0].bias.data = param_dict["conv1_b"]
        self.model.conv2[0].weight.data = param_dict["conv2_w"]
        self.model.conv2[0].bias.data = param_dict["conv2_b"]
        self.model.out.weight.data = param_dict["fc_w"]
        self.model.out.bias.data = param_dict["fc_b"]
        self.server_version = server_ptr[2]
        load_time_end = time.time()
        self.cs_info["loading_time"] = load_time_end - load_time_start

        self.model_lock.release(), self.export_lock["i"].release(), self.export_lock["f"].release()

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

    def federate_algo(self, mode="none"):
        weight = self.generate_federation_weight(mode)
        self.model.conv1[0].weight.data = self.weighted_sum(self.client_model_cache["conv1_w"], weight)
        self.model.conv1[0].bias.data = self.weighted_sum(self.client_model_cache["conv1_b"], weight)
        self.model.conv2[0].weight.data = self.weighted_sum(self.client_model_cache["conv2_w"], weight)
        self.model.conv2[0].bias.data = self.weighted_sum(self.client_model_cache["conv2_b"], weight)
        self.model.out.weight.data = self.weighted_sum(self.client_model_cache["fc_w"], weight)
        self.model.out.bias.data = self.weighted_sum(self.client_model_cache["fc_b"], weight)
        self.model.test(self.test_data)
        self.dummy_content += "Achieve average accuracy of " + str(self.model.accuracy) + "\n"

    def weighted_sum(self, list_of_data, weight):
        res = list_of_data[0] * weight[0]
        for i in range(1, len(weight)):
            res += list_of_data[i] * weight[i]
        return res

    def generate_federation_weight(self, mode="none", poly_factor=2):
        l = len(self.client_model_cache["server_version"])
        weight = []
        if mode == "none":
            weight = [1 for i in range(l)]

        if mode == "linear":
            weight = [-self.version + self.client_model_cache["server_version"][i]+self.client_model_cache["data_size"][i]+1 for i in range(l)]

        if mode == "polynomial":
            weight = [(-self.version + self.client_model_cache["server_version"][i]+self.client_model_cache["data_size"][i]+1)**poly_factor for i in range(l)]

        if mode == "exponential":
            weight = [math.exp(-self.version + self.client_model_cache["server_version"][i]+self.client_model_cache["data_size"][i]+1) for i in range(l)]

        return [ele / sum(weight) for ele in weight]

    def _step(self, args):
        self.dummy_content += self.uuid + " " + str(self.version) + " updated at " + str(time.ctime(time.time())) + "\n"
        # train model
        step_time_start = time.time()
        self.model.step(self.train_data)
        step_time_end = time.time()
        self.cs_info["epoch_time"] = step_time_end - step_time_start
        self.cs_info["train_one_time"] = self.cs_info["epoch_time"] / self.cs_info["data_size"]
        self.version += 1


class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.conv1 = nn.Sequential(
            nn.Conv2d(
                in_channels=1,
                out_channels=16,
                kernel_size=5,
                stride=1,
                padding=2,
            ),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2),
        )
        self.conv2 = nn.Sequential(
            nn.Conv2d(16, 32, 5, 1, 2),
            nn.ReLU(),
            nn.MaxPool2d(2),
        )
        # fully connected layer, output 10 classes
        self.out = nn.Linear(32 * 7 * 7, 10)
        self.optimizer = optim.Adam(self.parameters(), lr=0.01)
        self.loss_func = nn.CrossEntropyLoss()
        self.accuracy = 0

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        # flatten the output of conv2 to (batch_size, 32 * 7 * 7)
        x = x.view(x.size(0), -1)
        output = self.out(x)
        return output

    def step(self, ds):
        for data, target in ds:
            time.sleep(REST_TIME)
            self.optimizer.zero_grad()
            output = self(data)
            loss = self.loss_func(output, target)
            loss.backward()
            self.optimizer.step()

    def test(self, ds):
        total_ele = 0
        correct = 0
        for data, target in ds:
            total_ele += len(target)
            output = self(data)
            pred = output.data.max(1, keepdim=True)[1]
            correct += pred.eq(target.data.view_as(pred)).cpu().sum()
        self.accuracy = correct / total_ele * 100