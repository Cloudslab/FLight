from .base import BaseTask
from federatedLearning.communicate.router import router_factory

class federatedLearning0(BaseTask):
    def __init__(self):
        super().__init__(taskID=231, taskName='FederatedLearning0')

    def exec(self, inputData):
        router_factory.get_router((inputData["self_addr"],12345))