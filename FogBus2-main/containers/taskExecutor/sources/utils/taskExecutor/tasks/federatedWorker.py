from .base import BaseTask

class FederatedWorker(BaseTask):
    def __init__(self):
        super().__init__(taskID=220, taskName='FederatedWorker')

    def exec(self, inputData):
        inputData["worker_addr"] = inputData["self_addr"]
        return inputData