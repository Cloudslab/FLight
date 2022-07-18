from .base import BaseTask

class FederatedWorker0(BaseTask):
    def __init__(self):
        super().__init__(taskID=200, taskName='FederatedWorker0')

    def exec(self, inputData):

        inputData["taskID0"] = self.taskID

        return inputData