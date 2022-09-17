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
from .federated_learning.handler.rpc_handler import rpc_handler

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

        import sklearn
        address, port = self.addr[0], inputData["participants"][self.taskName]["data"]["port"]
        addr, r = router_factory.get_router((address, port))
        ftp_server_factory.set_ftp_server((address, port))
        r.add_handler("relation__", relationship_handler())
        r.add_handler("communicat", model_communication_handler())
        r.add_handler("rpc_call__", rpc_handler())

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
        mmm = sklearn.linear_model.LinearRegression()

        inputData = {"final_model": model.export(), "client": model.client, "path": model.client_model, "SKLEARN":str(mmm)}

        return inputData




    """
    def __init__(self):
        super().__init__(taskID=221, taskName='FederatedServer')
        self.worker_addr = []
        self.server_addr = None
        self.num_clients = 0
    def exec(self, inputData):
        self.server_addr = inputData["self_addr"]
        self.worker_addr.append(inputData["child_addr"])
        if not self.num_clients:
            self.num_clients = inputData["participants"][self.taskName]["data"]["client_num"]

        if len(self.worker_addr) < self.num_clients:
            return

        # set up router
        address = self.server_addr[0]
        port = inputData["participants"][self.taskName]["data"]["port"]

        addr, r = router_factory.get_router((address, port))
        r.add_handler("add_client", add_client_handler())
        r.add_handler("ack_ready_", ack_ready_handler())
        r.add_handler("ask_next__", ack_next_handler())
        r.add_handler("fetch_____", fetch_handler())
        r.add_handler("push______", push_handler())

        # set up model

        model = inputData["participants"][self.taskName]["data"]["model"]
        if model == "lr":
            model = linear_regression(
                inputData["participants"][self.taskName]["data"]["w"],
                inputData["participants"][self.taskName]["data"]["b"],
                inputData["participants"][self.taskName]["data"]["lr"]
            )
        tim = inputData["participants"][self.taskName]["data"]["tim"]
        itr_server = inputData["participants"][self.taskName]["data"]["itr_server"]
        itr_client = inputData["participants"][self.taskName]["data"]["itr_client"]

        for addr in self.worker_addr:
            model.add_client(addr)

        while len(model.client) < self.num_clients and model.ready_to_train_client < self.num_clients:
            time.sleep(WAITING_TIME_SLOT)

        for i in range(itr_server):

            for time_until_next_itr in range(tim):
                inputData["debug_logger"].info("Have {} seconds until next iteration:".format(tim-time_until_next_itr))
                time.sleep(1)

            version = model.version
            while len(model.client) < self.num_clients and model.ready_to_train_client < self.num_clients:
                time.sleep(WAITING_TIME_SLOT)
            model.ask_next(itr_client)
            while model.version == version:
                time.sleep(WAITING_TIME_SLOT)
            inputData["debug_logger"].info("----------------------------------MODEL---------------------------------")
            w, b, lr, version, id = model.export()

            inputData["debug_logger"].info("     w: {}".format(w))
            inputData["debug_logger"].info("     b: {}".format(b))
            inputData["debug_logger"].info("     lr: {}".format(lr))
            inputData["debug_logger"].info("     version: {}".format(version))
            inputData["debug_logger"].info("     id: {}".format(id))
            inputData["debug_logger"].info("----------------------------------MODEL---------------------------------")
        #

        inputData = {"final_model": model.export(), "twf": self.worker_addr}
        return inputData
        """
