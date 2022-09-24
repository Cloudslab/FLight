from .base import BaseTask

from .federated_learning.communicate.router import router_factory, ftp_server_factory

from .federated_learning.handler.relationship_handler import relationship_handler
from .federated_learning.federaed_learning_model.base import base_model
from .federated_learning.federaed_learning_model.synchronous_linear_regression import linear_regression
from .federated_learning.federaed_learning_model.synchronous_cv import synchronous_computer_vision
from .federated_learning.handler.model_communication_handler import model_communication_handler
from .federated_learning.handler.remote_call_handler import remote_call_handler

import time

WAITING_TIME_SLOT = 0.01

class FederatedServer(BaseTask):
    def __init__(self):
        super().__init__(taskID=221, taskName='FederatedServer')
        self.potential_client_addr = []
        self.addr = None
        self.num_clients = 0

    def exec(self, inputData):

        self.addr = inputData["self_addr"]
        self.potential_client_addr.append(inputData["child_addr"])
        self.num_clients = inputData["participants"][self.taskName]["data"]["client_num"]

        if len(self.potential_client_addr) < self.num_clients:
            return
        # set up router
        address, port = self.addr[0], inputData["participants"][self.taskName]["data"]["port"]
        addr, r = router_factory.get_router((address, port))
        ftp_server_factory.set_ftp_server((address, port))
        r.add_handler("relation__", relationship_handler())
        r.add_handler("communicat", model_communication_handler())
        r.add_handler("cli_step__", remote_call_handler())

        print(123)
        time_1 = time.time()
        # set up model
        model = synchronous_computer_vision()
        for i in range(3):
            model.add_client(self.potential_client_addr[0], i)
        for i in range(3,6):
            model.add_client(self.potential_client_addr[1], i)
        for i in range(6,9):
            model.add_client(self.potential_client_addr[2], i)

        print(1234)

        while (len(model.client) + len(model.server)) < 9:
            time.sleep(WAITING_TIME_SLOT)

        for i in range(10):
            print(i)
            for cli in model.get_client():
                if model.eligible_client(cli):
                    model.step_client(cli, 20)

            while not model.can_federate():
                time.sleep(0.01)
            model.federate()
            print("Average Accuracy: {}", model.cv1.accuracy)
            if model.cv1.accuracy >= 0.8:
                break
            time.sleep(0.01)  # time until next round
        time_2 = time.time()

        time_3 = time.time()
        modell = synchronous_computer_vision(19)
        while modell.cv1.accuracy <= 0.8:
            modell.cv1.step(modell.train_data)
        time_4 = time.time()

        inputData = {"logs": model.dummy_content, "time_fl": time_2 - time_1, "time_linear": time_4-time_3}

        return inputData
