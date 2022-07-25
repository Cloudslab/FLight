from .base import BaseTask

class FederatedServer(BaseTask):
    def __init__(self):
        super().__init__(taskID=221, taskName='FederatedServer')

    def exec(self, inputData):
        return inputData