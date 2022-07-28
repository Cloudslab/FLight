from federatedLearning.communicate.router import router
from federatedLearning.communicate.router import router_factory
from federatedLearning.federaed_learning_model.linear_regression import linear_regression
from federatedLearning.handler.add_client_handler import add_client_handler

if __name__ == "__main__":
    router_factory.set_router(("127.0.0.1", 12345))
    router_factory.get_router(("127.0.0.1", 12345)).add_handler("add_client", add_client_handler())
    lr = linear_regression(0, 0, 0.1)
    print(lr.uuid)

    lr.add_client(("127.0.0.1",12345))
    lr.add_client(("127.0.0.1", 12345))