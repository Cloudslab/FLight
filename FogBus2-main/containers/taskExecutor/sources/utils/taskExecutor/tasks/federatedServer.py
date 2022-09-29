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
from .federated_learning.federaed_learning_model.datawarehouse import data_warehouse

import time
import random

WAITING_TIME_SLOT = 0.01

class FederatedServer(BaseTask):
    def __init__(self):
        super().__init__(taskID=221, taskName='FederatedServer')
        self.potential_client_addr = []
        self.addr = None
        self.num_clients = 0
        self.machine_profile = {}

    def exec(self, inputData):

        self.addr = inputData["self_addr"]
        self.potential_client_addr.append(inputData["child_addr"])
        self.num_clients = inputData["participants"][self.taskName]["data"]["client_num"]
        self.machine_profile[inputData["child_addr"]] = inputData["machine_profile"]["cpu"], inputData["machine_profile"]["memory"]

        if len(self.potential_client_addr) < self.num_clients:
            return
        # set up router
        address, port = self.addr[0], inputData["participants"][self.taskName]["data"]["port"]
        addr, r = router_factory.get_router((address, port))
        ftp_server_factory.set_ftp_server((address, port))
        r.add_handler("relation__", relationship_handler())
        r.add_handler("communicat", model_communication_handler())
        r.add_handler("cli_step__", remote_call_handler())

        inputData = {"info": self.machine_profile}


        #minst_time_stamp100, minst_time_diff100, minst_accuracy100 = cifar_federated_learning_random_cs_no_even(self.potential_client_addr, 10)
        #minst_time_stamp300, minst_time_diff300, minst_accuracy300 = cifar_federated_learning_random_cs_no_even(self.potential_client_addr, 30)
        #inputData = {
        #    "minst_time_stamp100": minst_time_stamp100,
        #    "minst_time_diff100": minst_time_diff100,
        #    "minst_accuracy100": minst_accuracy100,
        #    "minst_time_stamp300": minst_time_stamp300,
        #    "minst_time_diff300": minst_time_diff300,
        #    "minst_accuracy300": minst_accuracy300
        #}

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

def minst_federated_learning_random_cs_no_even(client_addrs, amount):
    model = minst_classification()
    model.synchronous_federate_minimum_client = 3
    if amount == 10:
        for i in range(3):
            model.add_client(client_addrs[0], (i, 3))
        for i in range(3, 6):
            model.add_client(client_addrs[1], (i, 6))
        for i in range(6, 10):
            model.add_client(client_addrs[2], (i, 10))

    if amount == 30:
        for i in range(10):
            model.add_client(client_addrs[0], (i, 10))
        for i in range(10, 20):
            model.add_client(client_addrs[1], (i, 20))
        for i in range(20, 30):
            model.add_client(client_addrs[2], (i, 30))

    while len(model.get_client()) < amount:
        time.sleep(WAITING_TIME_SLOT)

    time_stamp = [time.time()]
    time_diff = [0]
    accuracy = [model.model.accuracy]
    for i in range(100):
        for cli in random.sample(model.get_client(), 3):
            model.step_client(cli, 10)
        while not model.can_federate():
            time.sleep(0.01)
        model.federate()
        time_stamp.append(time.time())
        time_diff.append(time_stamp[-1] - time_stamp[-2])
        accuracy.append(model.model.accuracy.item())

    return time_stamp, time_diff, accuracy

def cifar_federated_learning_random_cs_no_even(client_addrs, amount):
    model = cifar10_classification()
    model.synchronous_federate_minimum_client = 3
    if amount == 10:
        for i in range(3):
            model.add_client(client_addrs[0], (i, 30))
        for i in range(3, 6):
            model.add_client(client_addrs[1], (i, 60))
        for i in range(6, 10):
            model.add_client(client_addrs[2], (i, 100))

    if amount == 30:
        for i in range(10):
            model.add_client(client_addrs[0], (i, 100))
        for i in range(10, 20):
            model.add_client(client_addrs[1], (i, 200))
        for i in range(20, 30):
            model.add_client(client_addrs[2], (i, 300))

    while len(model.get_client()) < amount:
        time.sleep(WAITING_TIME_SLOT)

    time_stamp = [time.time()]
    time_diff = [0]
    accuracy = [model.model.accuracy]
    for i in range(100):
        for cli in random.sample(model.get_client(), 3):
            model.step_client(cli, 5)
        while not model.can_federate():
            time.sleep(0.01)
        model.federate()
        time_stamp.append(time.time())
        time_diff.append(time_stamp[-1] - time_stamp[-2])
        accuracy.append(model.model.accuracy.item())

    return time_stamp, time_diff, accuracy

def minst_federated_learning_no_cs_no_even(client_addrs, amount):
    model = minst_classification()
    model.synchronous_federate_minimum_client = amount
    if amount == 10:
        for i in range(3):
            model.add_client(client_addrs[0], (i,3))
        for i in range(3,6):
            model.add_client(client_addrs[1], (i,6))
        for i in range(6,10):
            model.add_client(client_addrs[2], (i,10))

    if amount == 30:
        for i in range(10):
            model.add_client(client_addrs[0], (i,10))
        for i in range(10,20):
            model.add_client(client_addrs[1], (i,20))
        for i in range(20,30):
            model.add_client(client_addrs[2], (i,30))

    while len(model.get_client()) < amount:
        time.sleep(WAITING_TIME_SLOT)

    time_stamp = [time.time()]
    time_diff = [0]
    accuracy = [model.model.accuracy]
    for i in range(100):
        for cli in model.get_client():
            model.step_client(cli, 10)
        while not model.can_federate():
            time.sleep(0.01)
        model.federate()
        time_stamp.append(time.time())
        time_diff.append(time_stamp[-1]-time_stamp[-2])
        accuracy.append(model.model.accuracy.item())

    return time_stamp, time_diff, accuracy

def cifar_federated_learning_no_cs_no_even(client_addrs, amount):
    model = cifar10_classification()
    model.synchronous_federate_minimum_client = amount
    if amount == 10:
        for i in range(3):
            model.add_client(client_addrs[0], (i*10,30))
        for i in range(3,6):
            model.add_client(client_addrs[1], (i*10,60))
        for i in range(6,10):
            model.add_client(client_addrs[2], (i*10,100))

    if amount == 30:
        for i in range(10):
            model.add_client(client_addrs[0], (i*10,100))
        for i in range(10,20):
            model.add_client(client_addrs[1], (i*10,200))
        for i in range(20,30):
            model.add_client(client_addrs[2], (i*10,300))

    while len(model.get_client()) < amount:
        time.sleep(WAITING_TIME_SLOT)

    time_stamp = [time.time()]
    time_diff = [0]
    accuracy = [model.model.accuracy]
    for i in range(50):
        for cli in model.get_client():
            model.step_client(cli, 5)
        while not model.can_federate():
            time.sleep(0.01)
        model.federate()
        time_stamp.append(time.time())
        time_diff.append(time_stamp[-1]-time_stamp[-2])
        accuracy.append(model.model.accuracy.item())

    return time_stamp, time_diff, accuracy

def minst_federated_learning_no_cs_even(client_addrs, amount):
    model = minst_classification()
    model.synchronous_federate_minimum_client = amount
    if amount == 10:
        for i in range(3):
            model.add_client(client_addrs[0], (i,i+1))
        for i in range(3,6):
            model.add_client(client_addrs[1], (i,i+1))
        for i in range(6,10):
            model.add_client(client_addrs[2], (i,i+1))

    if amount == 30:
        for i in range(10):
            model.add_client(client_addrs[0], (i,i+1))
        for i in range(10,20):
            model.add_client(client_addrs[1], (i,i+1))
        for i in range(20,30):
            model.add_client(client_addrs[2], (i,i+1))

    while len(model.get_client()) < amount:
        time.sleep(WAITING_TIME_SLOT)

    time_stamp = [time.time()]
    time_diff = [0]
    accuracy = [model.model.accuracy]
    for i in range(100):
        for cli in model.get_client():
            model.step_client(cli, 10)
        while not model.can_federate():
            time.sleep(0.01)
        model.federate()
        time_stamp.append(time.time())
        time_diff.append(time_stamp[-1]-time_stamp[-2])
        accuracy.append(model.model.accuracy.item())

    return time_stamp, time_diff, accuracy

def cifar_federated_learning_no_cs_even(client_addrs, amount):
    model = cifar10_classification()
    model.synchronous_federate_minimum_client = amount
    if amount == 10:
        for i in range(3):
            model.add_client(client_addrs[0], (i*10,(i+1)*10))
        for i in range(3,6):
            model.add_client(client_addrs[1], (i*10,(i+1)*10))
        for i in range(6,10):
            model.add_client(client_addrs[2], (i*10,(i+1)*10))

    if amount == 30:
        for i in range(10):
            model.add_client(client_addrs[0], (i*10,(i+1)*10))
        for i in range(10,20):
            model.add_client(client_addrs[1], (i*10,(i+1)*10))
        for i in range(20,30):
            model.add_client(client_addrs[2], (i*10,(i+1)*10))

    while len(model.get_client()) < amount:
        time.sleep(WAITING_TIME_SLOT)

    time_stamp = [time.time()]
    time_diff = [0]
    accuracy = [model.model.accuracy]
    for i in range(50):
        for cli in model.get_client():
            model.step_client(cli, 5)
        while not model.can_federate():
            time.sleep(0.01)
        model.federate()
        time_stamp.append(time.time())
        time_diff.append(time_stamp[-1]-time_stamp[-2])
        accuracy.append(model.model.accuracy.item())

    return time_stamp, time_diff, accuracy

def minst_sequential_test(client_addr, amount):
    model = minst_classification()
    model.synchronous_federate_minimum_client = 1
    model.add_client(client_addr, (0,amount))
    while len(model.get_client()) == 0:
        time.sleep(WAITING_TIME_SLOT)

    time_stamp = [time.time()]
    time_diff = [0]
    accuracy = [model.model.accuracy]

    for i in range(100):
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

    for i in range(100):
        model.step_client(model.get_client()[0], 5)
        while not model.can_federate():
            time.sleep(0.01)
        model.federate()
        time_stamp.append(time.time())
        time_diff.append(time_stamp[-1]-time_stamp[-2])
        accuracy.append(model.model.accuracy.item())

    return time_stamp, time_diff, accuracy

