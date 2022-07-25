from .base import BaseTask

class FederatedServer(BaseTask):
    def __init__(self):
        super().__init__(taskID=221, taskName='FederatedServer')
        self.worker_addr = []

    def exec(self, inputData):

        self.worker_addr.append(inputData["child_addr"])
        inputData["worker_addr"] = self.worker_addr
        return inputData