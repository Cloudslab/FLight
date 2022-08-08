from .base import BaseTask

from .federated_learning.communicate.router import router_factory
from .federated_learning.federaed_learning_model.linear_regression import linear_regression
from .federated_learning.handler.add_client_handler import add_client_handler
from .federated_learning.handler.ack_ready_handler import ack_ready_handler
from .federated_learning.handler.ask_next_handler import ack_next_handler
from .federated_learning.handler.fetch_handler import fetch_handler
from .federated_learning.handler.push_handler import push_handler

import time
import socket

from .federated_learning.federaed_learning_model.datawarehouse import data_warehouse

LOCAL_TRAIN_ITERATION = 10
GLOBAL_TRAIN_ITERATION = 100
WAITING_TIME_SLOT = 0.01

class FederatedServer(BaseTask):
    def __init__(self):
        super().__init__(taskID=221, taskName='FederatedServer')
        self.worker_addr = []
        self.server_addr = None
        self.num_clients = 0
    def exec(self, inputData):
        self.server_addr = inputData["self_addr"]
        self.worker_addr.append(inputData["child_addr"])
        if not self.num_clients:
            self.num_clients = inputData["participants"][self.taskName]["data"]["client_num"]

        if len(self.worker_addr) < self.num_clients:
            return
        """
        router_factory.set_router((self.server_addr[0], 54324))
        router_factory.get_router((self.server_addr[0], 54324)).add_handler("add_client", add_client_handler())
        router_factory.get_router((self.server_addr[0], 54324)).add_handler("ack_ready_", ack_ready_handler())
        router_factory.get_router((self.server_addr[0], 54324)).add_handler("ask_next__", ack_next_handler())
        router_factory.get_router((self.server_addr[0], 54324)).add_handler("fetch_____", fetch_handler())
        router_factory.get_router((self.server_addr[0], 54324)).add_handler("push______", push_handler())

        lr = linear_regression(0, 0, 0.01)
        #for (addr, port) in self.worker_addr:
        lr.add_client((self.server_addr[0], 54321))
        lr.add_client((self.server_addr[0], 54322))
        lr.add_client((self.server_addr[0], 54323))


        while len(lr.client) < self.num_clients and lr.ready_to_train_client < self.num_clients:
            time.sleep(WAITING_TIME_SLOT)

        for i in range(GLOBAL_TRAIN_ITERATION):
            version = lr.version
            while len(lr.client) < self.num_clients and lr.ready_to_train_client < self.num_clients:
                time.sleep(WAITING_TIME_SLOT)
            lr.ask_next(LOCAL_TRAIN_ITERATION)
            while  lr.version == version:
                time.sleep(WAITING_TIME_SLOT)
        #
        inputData["Ress"] = {"final_model": lr.export(), "final_clients":lr.client, "twf": self.worker_addr}
        """
        i = {}
        i["self"] = inputData["self_addr"]
        i["name"] = self.taskName
        i["child"] = self.worker_addr
        return i
