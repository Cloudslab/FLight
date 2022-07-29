from .base import BaseTask
from federatedLearning.communicate.router import router_factory

class federatedLearning1(BaseTask):
    def __init__(self):
        super().__init__(taskID=232, taskName='FederatedLearning1')

    def exec(self, inputData):
        router_factory.get_router((inputData["self_addr"],12345))