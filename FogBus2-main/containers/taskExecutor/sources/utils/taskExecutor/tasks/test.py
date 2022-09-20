from threading import Thread

from federated_learning.federaed_learning_model.synchronous_linear_regression import linear_regression
from federated_learning.federaed_learning_model.base import base_model
from federated_learning.federaed_learning_model.synchronous_cv import synchronous_computer_vision

from federated_learning.federaed_learning_model.datawarehouse import model_warehouse, data_warehouse
from federated_learning.communicate.router import router_factory, ftp_server_factory
from federated_learning.handler.relationship_handler import relationship_handler
from federated_learning.handler.model_communication_handler import model_communication_handler
from federated_learning.handler.remote_call_handler import remote_call_handler

import time

import glob

if __name__ == "__main__":

    addr, r = router_factory.get_router(("127.0.0.1", 12345))
    ftp_addr, ftp_server = ftp_server_factory.get_ftp_server(("127.0.0.1", 12345))
    r.add_handler("relation__", relationship_handler())
    r.add_handler("communicat", model_communication_handler())
    r.add_handler("cli_step__", remote_call_handler())
    model = synchronous_computer_vision(0)
    for i in range(10):
        model.add_client(addr, i)
    while (len(model.client) + len(model.server) + len(model.peer)) < 10:
        time.sleep(0.01)

    m = model_warehouse()

    for i in range(10):
        print(i)
        for cli in model.get_client():
            if model.eligible_client(cli):
                model.step_client(cli, 20)

        while not model.can_federate():
            time.sleep(0.01)
        model.federate()
        print("Average Accuracy: {}", model.cv1.accuracy)
        time.sleep(3) # time until next round
    print(model.dummy_content)
    print("Done")
    # time.sleep(5)
    # print("------------------model_info")
    # print(model.dummy_content)
    # print("------------------model_param")
    # print(model.lr.linear.weight.data)
    # print(model.lr.linear.bias.data)
