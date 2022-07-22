from .base import BaseTask

class FederatedWorker(BaseTask):
    def __init__(self):
        super().__init__(taskID=220, taskName='FederatedWorker')

    def exec(self, inputData):

        inputData["number"] += 1
        if "addr" in inputData:
            inputData["ServerAddr"] = inputData["addr"]
        return inputData