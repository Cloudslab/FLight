from .base import BaseTask

from .federated_learning.communicate.router import router_factory, ftp_server_factory

from .federated_learning.handler.relationship_handler import relationship_handler
from .federated_learning.federaed_learning_model.base import base_model
from .federated_learning.federaed_learning_model.synchronous_linear_regression import linear_regression
from .federated_learning.federaed_learning_model.synchronous_cv import synchronous_computer_vision
from .federated_learning.handler.model_communication_handler import model_communication_handler
from .federated_learning.handler.remote_call_handler import remote_call_handler

from .federated_learning.federaed_learning_model.minst import minst_classification
from .federated_learning.federaed_learning_model.cifar10 import cifar10_classification

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

        time_stamp10, time_diff10, accuracy10 = minst_sequential_test(self.potential_client_addr[0], 10)
        time_stamp30, time_diff30, accuracy30 = minst_sequential_test(self.potential_client_addr[0], 30)
        inputData = {
            "time_stamp10": time_stamp10,
            "time_diff10": time_diff10,
            "accuracy10": accuracy10,
            "time_stamp30": time_stamp30,
            "time_diff30": time_diff30,
            "accuracy30": accuracy30
        }

        return inputData

        """

        # set up model
        model = synchronous_computer_vision()
        for i in range(3):
            model.add_client(self.potential_client_addr[0], i)
        for i in range(3,6):
            model.add_client(self.potential_client_addr[1], i)
        for i in range(6,9):
            model.add_client(self.potential_client_addr[2], i)

        model1 = synchronous_computer_vision()
        for i in range(3):
            model1.add_client(self.potential_client_addr[0], i)
        for i in range(3,9):
            model1.add_client(self.potential_client_addr[1], i)

        print(1234)

        while (len(model.client) + len(model.server)) < 9:
            time.sleep(WAITING_TIME_SLOT)

        while (len(model1.client) + len(model1.server)) < 9:
            time.sleep(WAITING_TIME_SLOT)

        time_1 = time.time()
        for i in range(100):
            print(i)
            for cli in model.get_client():
                if model.eligible_client(cli):
                    model.step_client(cli, 20)

            while not model.can_federate():
                time.sleep(0.01)
            model.federate()
            print("Average Accuracy: {}", model.cv1.accuracy)
            if model.cv1.accuracy >= 75:
                break
            time.sleep(0.01)  # time until next round
        time_2 = time.time()

        time_3 = time.time()
        for i in range(100):
            print(i)
            for cli in model1.get_client():
                if model1.eligible_client(cli):
                    model1.step_client(cli, 20)

            while not model1.can_federate():
                time.sleep(0.01)
            model1.federate()
            print("Average Accuracy: {}", model1.cv1.accuracy)
            if model1.cv1.accuracy >= 75:
                break
            time.sleep(0.01)  # time until next round
        time_4 = time.time()


        inputData = {"logs": [model.dummy_content, model1.dummy_content], "time": [time_2 - time_1, time_4 - time_3]}

        return inputData
    """

def minst_sequential_test(client_addr, amount):
    model = minst_classification()
    model.synchronous_federate_minimum_client = 1
    model.add_client(client_addr, (0,amount))
    while len(model.get_client()) == 0:
        time.sleep(WAITING_TIME_SLOT)

    time_stamp = [time.time()]
    time_diff = [0]
    accuracy = [model.model.accuracy]

    for i in range(1):
        model.step_client(model.get_client()[0], 1)
        while not model.can_federate():
            time.sleep(0.01)
        model.federate()
        time_stamp.append(time.time())
        time_diff.append(time_stamp[-1]-time_stamp[-2])
        accuracy.append(model.model.accuracy.item())

    return time_stamp, time_diff, accuracy

def cifar_sequential_test(client_addr, amount):
    model = cifar10_classification()
    model.synchronous_federate_minimum_client = 1
    model.add_client(client_addr, (0, amount))
    while len(model.get_client()) == 0:
        time.sleep(WAITING_TIME_SLOT)

    time_stamp = [time.time()]
    time_diff = [0]
    accuracy = [model.model.accuracy]

    for i in range(1):
        model.step_client(model.get_client()[0], 10)
        while not model.can_federate():
            time.sleep(0.01)
        model.federate()
        time_stamp.append(time.time())
        time_diff.append(time_stamp[-1]-time_stamp[-2])
        accuracy.append(model.model.accuracy)

    return time_stamp, time_diff, accuracy

