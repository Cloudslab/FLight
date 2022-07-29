from .base import BaseTask
from .federated_learning.communicate.router import router_factory

from .federated_learning.communicate.router import router_factory
from .federated_learning.federaed_learning_model.linear_regression import linear_regression
from .federated_learning.handler.add_client_handler import add_client_handler
from .federated_learning.handler.ack_ready_handler import ack_ready_handler
from .federated_learning.handler.ask_next_handler import ack_next_handler
from .federated_learning.handler.fetch_handler import fetch_handler
from .federated_learning.handler.push_handler import push_handler

class federatedLearning1(BaseTask):
    def __init__(self):
        super().__init__(taskID=232, taskName='FederatedLearning1')

    def exec(self, inputData):
        router_factory.get_router((inputData["self_addr"][0], 54322))
        router_factory.get_router((self.server_addr[0], 54322)).add_handler("add_client", add_client_handler())
        router_factory.get_router((self.server_addr[0], 54322)).add_handler("ack_ready_", ack_ready_handler())
        router_factory.get_router((self.server_addr[0], 54322)).add_handler("ask_next__", ack_next_handler())
        router_factory.get_router((self.server_addr[0], 54322)).add_handler("fetch_____", fetch_handler())
        router_factory.get_router((self.server_addr[0], 54322)).add_handler("push______", push_handler())
