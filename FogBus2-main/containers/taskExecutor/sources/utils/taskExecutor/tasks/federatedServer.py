from .base import BaseTask

from .federated_learning.communicate.router import router_factory
from .federated_learning.federaed_learning_model.linear_regression import linear_regression
from .federated_learning.handler.add_client_handler import add_client_handler
from .federated_learning.handler.ack_ready_handler import ack_ready_handler
from .federated_learning.handler.ask_next_handler import ack_next_handler
from .federated_learning.handler.fetch_handler import fetch_handler
from .federated_learning.handler.push_handler import push_handler

import time

from .federated_learning.federaed_learning_model.datawarehouse import data_warehouse
def one_x():
    return ([1,2,3,4,5],[1,2,3,4,5])

def two_x():
    return ([1,2,3,4,5],[2,4,6,8,10])

def three_x():
    return ([1,2,3,4,5],[3,6,9,12,15])

class FederatedServer(BaseTask):
    def __init__(self):
        super().__init__(taskID=221, taskName='FederatedServer')
        self.worker_addr = []
        self.server_addr = None
    def exec(self, inputData):
        self.server_addr = inputData["self_addr"]
        self.worker_addr.append(inputData["child_addr"])

        if len(self.worker_addr) < 3:
            return

        router_factory.set_router((self.server_addr[0], 54322))
        router_factory.get_router((self.server_addr[0], 54322)).add_handler("add_client", add_client_handler())
        router_factory.get_router((self.server_addr[0], 54322)).add_handler("ack_ready_", ack_ready_handler())
        router_factory.get_router((self.server_addr[0], 54322)).add_handler("ask_next__", ack_next_handler())
        router_factory.get_router((self.server_addr[0], 54322)).add_handler("fetch_____", fetch_handler())
        router_factory.get_router((self.server_addr[0], 54322)).add_handler("push______", push_handler())

        lr = linear_regression(0, 0, 0.01)
        for (addr, port) in self.worker_addr:
            lr.add_client((addr, port))
        while len(lr.client) < 3 and lr.ready_to_train_client < 3:
            time.sleep(0.1)
        #
        #
        data_warehouse.get(lr.client[0][0]).load_data = one_x
        data_warehouse.get(lr.client[1][0]).load_data = two_x
        data_warehouse.get(lr.client[2][0]).load_data = three_x
        #
        for i in range(100):
            while len(lr.client) < 3 and lr.ready_to_train_client < 3:
                time.sleep(0.01)
            lr.ask_next(10)
        #
        inputData["Ress"] = {"final_model": lr.export()}
        return inputData
