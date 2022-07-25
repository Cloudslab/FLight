from .base import BaseTask

class FederatedServer(BaseTask):
    def __init__(self):
        super().__init__(taskID=221, taskName='FederatedServer')

    def exec(self, inputData):
        inputData["server_addr"] = inputData["self_addr"]
        inputData["worker_addr"] = inputData["child_addr"]

        import socket

        HOST, PORT = inputData["child_addr"]

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT+10))
            s.sendall(b"Hello, world")
            data = s.recv(1024)
        inputData["finalRRR"] = data
        return inputData