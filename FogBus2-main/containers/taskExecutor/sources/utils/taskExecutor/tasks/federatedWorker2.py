from .base import BaseTask


class FederatedWorker2(BaseTask):
    def __init__(self):
        super().__init__(taskID=202, taskName='FederatedWorker2')

    def exec(self, inputData):

        inputData["taskID2"] = self.taskID

        return inputData