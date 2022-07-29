from .base import BaseTask
from federatedLearning.communicate.router import router_factory

class federatedLearning2(BaseTask):
    def __init__(self):
        super().__init__(taskID=233, taskName='FederatedLearning2')

    def exec(self, inputData):
        #router_factory.get_router((inputData["self_addr"][0],54321))
        pass