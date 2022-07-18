from .base import BaseTask

class FederatedWorker1(BaseTask):
    def __init__(self):
        super().__init__(taskID=201, taskName='FederatedWorker1')

    def exec(self, inputData):

        inputData["taskID1"] = self.taskID

        return inputData