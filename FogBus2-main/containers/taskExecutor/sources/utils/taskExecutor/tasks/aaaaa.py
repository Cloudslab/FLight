from time import sleep

from federatedLearning.communicate.router import router
from federatedLearning.communicate.router import router_factory
from federatedLearning.federaed_learning_model.linear_regression import linear_regression
from federatedLearning.handler.add_client_handler import add_client_handler
from federatedLearning.handler.ack_ready_handler import ack_ready_handler

from federatedLearning.federaed_learning_model.datawarehouse import data_warehouse

if __name__ == "__main__":
    router_factory.set_router(("127.0.0.1", 12345))
    router_factory.get_router(("127.0.0.1", 12345)).add_handler("add_client", add_client_handler())
    router_factory.get_router(("127.0.0.1", 12345)).add_handler("ack_ready_", ack_ready_handler())

    lr = linear_regression(0, 0, 0.1)

    lr.add_client(("127.0.0.1",12345))
    lr.add_client(("127.0.0.1",12345))
    lr.add_client(("127.0.0.1", 12345))

    while len(lr.client) < 3:
        sleep(0.1)

    lr.ask_next(1,1,1)

    dd = data_warehouse()
    print("debug")