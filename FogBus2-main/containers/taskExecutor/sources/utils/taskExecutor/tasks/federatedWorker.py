from .base import BaseTask

class FederatedWorker(BaseTask):
    def __init__(self):
        super().__init__(taskID=220, taskName='FederatedWorker')

    def exec(self, inputData):
        print("worker exec")