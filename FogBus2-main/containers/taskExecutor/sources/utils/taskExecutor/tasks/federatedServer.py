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

        address = self.server_addr[0]
        port = inputData["participants"][self.taskName]["data"]["port"]

        addr, r = router_factory.get_router((address, port))
        r.add_handler("add_client", add_client_handler())
        r.add_handler("ack_ready_", ack_ready_handler())
        r.add_handler("ask_next__", ack_next_handler())
        r.add_handler("fetch_____", fetch_handler())
        r.add_handler("push______", push_handler())

        lr = linear_regression(0, 0, 0.01)

        data_warehouse.insert_xy(1,1)
        #for (addr, port) in self.worker_addr:
        for addr in self.worker_addr:
            lr.add_client(addr)


        while len(lr.client) < self.num_clients and lr.ready_to_train_client < self.num_clients:
            time.sleep(WAITING_TIME_SLOT)

        for i in range(GLOBAL_TRAIN_ITERATION):
            """
            for time_until_next_itr in range(20):
                inputData["debug_logger"].info("Have {} seconds until next iteration:".format(20-time_until_next_itr))
                time.sleep(1)
            """

            version = lr.version
            while len(lr.client) < self.num_clients and lr.ready_to_train_client < self.num_clients:
                time.sleep(WAITING_TIME_SLOT)
            lr.ask_next(LOCAL_TRAIN_ITERATION)
            while  lr.version == version:
                time.sleep(WAITING_TIME_SLOT)
        #
        
        inputData = {"final_model": lr.export(), "twf": self.worker_addr}
        return inputData
