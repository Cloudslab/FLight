from .base import BaseTask

from .federated_learning.communicate.router import router_factory, ftp_server_factory
from .federated_learning.federaed_learning_model.linear_regression import linear_regression
from .federated_learning.handler.add_client_handler import add_client_handler
from .federated_learning.handler.ack_ready_handler import ack_ready_handler
from .federated_learning.handler.ask_next_handler import ack_next_handler
from .federated_learning.handler.fetch_handler import fetch_handler
from .federated_learning.handler.push_handler import push_handler

from .federated_learning.handler.relationship_handler import relationship_handler
from .federated_learning.federaed_learning_model.base import base_model
from .federated_learning.handler.model_communication_handler import model_communication_handler

import time

WAITING_TIME_SLOT = 0.01

class FederatedServer(BaseTask):
    def __init__(self):
        super().__init__(taskID=221, taskName='FederatedServer')
        self.potential_client_addr = []
        self.addr = None
        self.num_clients = 0
        #self.nn = torch.nn.Conv2d(1, 32, 3, 1)

    def exec(self, inputData):


        self.addr = inputData["self_addr"]
        self.potential_client_addr.append(inputData["child_addr"])
        self.num_clients = inputData["participants"][self.taskName]["data"]["client_num"]

        if len(self.potential_client_addr) < self.num_clients:
            return
        # set up router
        address, port = self.addr[0], inputData["participants"][self.taskName]["data"]["port"]
        addr, r = router_factory.get_router((address, port))
        ftp_server_factory.set_ftp_server((address, port))
        r.add_handler("relation__", relationship_handler())
        r.add_handler("communicat", model_communication_handler())

        # set up model
        model = base_model()
        model.add_client(self.potential_client_addr[0])
        model.add_client(self.potential_client_addr[1])
        model.add_server(self.potential_client_addr[2])

        while (len(model.client) + len(model.server)) < self.num_clients:
            time.sleep(WAITING_TIME_SLOT)
        i = 6
        for cli in model.get_client():
            model.step_remote(cli, "s", i)
            i += 6
        for ser in model.get_server():
            model.step_remote(ser, "c", 6)
        while (len(model.get_remote_fetch_model_credential("s")) + len(
                model.get_remote_fetch_model_credential("c"))) < 2:
            time.sleep(0.01)
        for cre in model.get_remote_fetch_model_credential("s"):
            model.download_model(cre, "s")
        for cre in model.get_remote_fetch_model_credential("c"):
            model.download_model(cre, "c")

        #while len(model.client_model.keys()) < self.num_clients:
        #    time.sleep(WAITING_TIME_SLOT)

        inputData = {"final_model": model.export(), "client": model.client, "path": model.client_model}

        return inputData
