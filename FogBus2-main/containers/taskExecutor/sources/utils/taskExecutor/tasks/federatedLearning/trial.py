from communicate.router import router
from communicate.router import router_factory
from federaed_learning_model.linear_regression import linear_regression

if __name__ == "__main__":
    router_factory.get_router(("127.0.0.1", 12345))
