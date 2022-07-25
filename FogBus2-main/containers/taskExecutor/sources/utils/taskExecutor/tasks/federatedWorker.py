from .base import BaseTask

class FederatedWorker(BaseTask):
    def __init__(self):
        super().__init__(taskID=220, taskName='FederatedWorker')

    def exec(self, inputData):
        inputData["worker_addr"] = inputData["self_addr"]
        import socket

        HOST, PORT = inputData["self_addr"]

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
                data = conn.recv(1024)
                #conn.sendall(data)