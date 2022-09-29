from threading import Thread

from federated_learning.federaed_learning_model.synchronous_linear_regression import linear_regression
from federated_learning.federaed_learning_model.base import base_model
from federated_learning.federaed_learning_model.synchronous_cv import synchronous_computer_vision

from federated_learning.federaed_learning_model.datawarehouse import model_warehouse, data_warehouse
from federated_learning.communicate.router import router_factory, ftp_server_factory
from federated_learning.handler.relationship_handler import relationship_handler
from federated_learning.handler.model_communication_handler import model_communication_handler
from federated_learning.handler.remote_call_handler import remote_call_handler

from federated_learning.federaed_learning_model.minst import minst_classification
from federated_learning.federaed_learning_model.cifar10 import cifar10_classification

import time

import glob

def minst_federated_learning_random_cs_no_even(client_addr, amount):
    import random
    model = minst_classification()
    model.synchronous_federate_minimum_client = amount
    if amount == 10:
        for i in range(3):
            model.add_client(client_addr, (i, 3))
        for i in range(3, 6):
            model.add_client(client_addr, (i, 6))
        for i in range(6, 10):
            model.add_client(client_addr, (i, 10))

    if amount == 30:
        for i in range(10):
            model.add_client(client_addr, (i, 10))
        for i in range(10, 20):
            model.add_client(client_addr, (i, 20))
        for i in range(20, 30):
            model.add_client(client_addr, (i, 30))

    while len(model.get_client()) < amount:
        time.sleep(0.01)

    time_stamp = [time.time()]
    time_diff = [0]
    accuracy = [model.model.accuracy]
    for i in range(1):
        for cli in model.get_client():
            model.step_client(cli, 10)
        while not model.can_federate():
            time.sleep(0.01)
        model.federate()
        time_stamp.append(time.time())
        time_diff.append(time_stamp[-1] - time_stamp[-2])
        accuracy.append(model.model.accuracy.item())
        print(time_diff[-1])
        print(accuracy[-1])

    for cli, val in model.client_performance.items():
        print(cli)
        for k, v in val.items():
            print(k,v)
    return time_stamp, time_diff, accuracy

def cifar_federated_learning_random_cs_no_even(client_addr, amount):
    import random
    model = cifar10_classification()
    model.synchronous_federate_minimum_client = amount
    if amount == 10:
        for i in range(3):
            model.add_client(client_addr, (i, 30))
        for i in range(3, 6):
            model.add_client(client_addr, (i, 60))
        for i in range(6, 10):
            model.add_client(client_addr, (i, 100))

    if amount == 30:
        for i in range(10):
            model.add_client(client_addr, (i, 100))
        for i in range(10, 20):
            model.add_client(client_addr, (i, 200))
        for i in range(20, 30):
            model.add_client(client_addr, (i, 300))

    while len(model.get_client()) < amount:
        time.sleep(0.01)

    time_stamp = [time.time()]
    time_diff = [0]
    accuracy = [model.model.accuracy]
    for i in range(1):
        for cli in model.get_client():
            model.step_client(cli, 10)
        while not model.can_federate():
            time.sleep(0.01)
        model.federate()
        time_stamp.append(time.time())
        time_diff.append(time_stamp[-1] - time_stamp[-2])
        accuracy.append(model.model.accuracy.item())
        print(time_diff[-1])
        print(accuracy[-1])

    for cli, val in model.client_performance.items():
        print(cli)
        for k, v in val.items():
            print(k,v)
    return time_stamp, time_diff, accuracy


if __name__ == "__main__":

    addr, r = router_factory.get_router(("127.0.0.1", 12345))
    ftp_addr, ftp_server = ftp_server_factory.get_ftp_server(("127.0.0.1", 12345))
    r.add_handler("relation__", relationship_handler())
    r.add_handler("communicat", model_communication_handler())
    r.add_handler("cli_step__", remote_call_handler())

    #_,_, a = minst_federated_learning_no_cs_even([addr, addr, addr], 30)
    #print(a)

    cifar_federated_learning_random_cs_no_even(addr, 10)


