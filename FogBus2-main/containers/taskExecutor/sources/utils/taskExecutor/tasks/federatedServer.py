from .base import BaseTask

class FederatedServer(BaseTask):
    def __init__(self):
        super().__init__(taskID=221, taskName='FederatedServer')
        self.worker_addr = []
        self.server_addr = None
    def exec(self, inputData):
        self.server_addr = inputData["self_addr"]
        self.worker_addr.append(inputData["child_addr"])

        if len(self.worker_addr) >= 3:
            inputData["Ress"] = {"server_addr":self.server_addr, "worker_addr":self.worker_addr}
            return inputData
