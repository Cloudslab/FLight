from federatedLearning.communicate.router import router
from federatedLearning.communicate.router import router_factory
from federatedLearning.federaed_learning_model.linear_regression import linear_regression

if __name__ == "__main__":
    router_factory.set_router(("127.0.0.1", 12345))
    lr = linear_regression(0, 0, 0.1)

    lr.add_client(("127.0.0.1",12345))
    lr.add_client(("127.0.0.1", 12345))