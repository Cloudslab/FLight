"""
A routing is the singleton class which hold a communicator (../utils/component/communicator), it is expected that
all incoming and outgoing messages are through this class. This class is created instead of using communicator directly
to leave place for future extension.
"""
from abc import ABC

from ..utils.component.communicator import Communicator
from ..utils.component.communicator import ComponentRole
from ..utils.types.basic.address import Address
from ..utils.connection.message.received import MessageReceived
from typing import Tuple

from ..utils.connection.message.received import MessageReceived
from ..utils.connection.message.toSend import MessageToSend
from ..utils.types.message.type import MessageType
from ..utils.types.component.identitySerializable import Component
from ...warehouse.DataWarehouse import DataWarehouse

# from ...warehouse.DataWarehouse import DataWarehouse

# ToDo: read from .env

ADDRESS: Address = ["127.0.0.1", 5000]
PORT_RANGE = [5000, 5001]
LOG_LVL = 0
MASTER_ADDR = ["127.0.0.1", 5000]
RL_ADDR = ["127.0.0.1", 5000]

X = [1, 2, 3, 4, 5]
Y = [10, 20, 30, 40, 50]


class Router:
    class _Communicator(Communicator, ABC):
        def handleMessage(self, message: MessageReceived):
            # ToDo: add a dispatcher here
            from ...ml.model.LinearRegression import LinearRegressionFactory
            if message.data["id"] == "lr_init":  # receive create linear regression message

                local_model = LinearRegressionFactory().LinearRegressionClient(message.toDict()["data"]["pointer"],
                                                                               ["127.0.0.1", 5000])
                if local_model:
                    local_model.server_ptr.ack_client_ready(local_model.ptr)

            if message.data["id"] == "lr_ack":  # try to add it to local linear regression model
                ptr_dict = message.toDict()["data"]["pointer"]
                local_model = DataWarehouse().get(ptr_dict["remote_retriever_name"], ptr_dict["remote_id"])
                if local_model:
                    local_model.add_worker_pointer(message.toDict()["data"]["call_back_pointer"])

            if message.data[
                "id"] == "lr_step":  # if the local model agree to do a local training, fetch data from server
                client_model_ptr_dict, server_model_ptr_dict = \
                    message.toDict()["data"]["pointer"], message.toDict()["data"]["call_back_pointer"]

                client_model = DataWarehouse().get(client_model_ptr_dict["remote_retriever_name"],
                                                   client_model_ptr_dict["remote_id"])

                if client_model.available(server_model_ptr_dict):
                    client_model.fetch_server()

            if message.data["id"] == "lr_fetch_server":
                server_model_ptr_dict, client_model_ptr_dict = \
                    message.toDict()["data"]["pointer"], message.toDict()["data"]["call_back_pointer"]

                server_model = DataWarehouse().get(server_model_ptr_dict["remote_retriever_name"],
                                                   server_model_ptr_dict["remote_id"])
                if server_model and server_model.available_data(server_model_ptr_dict):
                    server_model.waiting_next_round += 1

            if message.data["id"] == "lr_server_data" and message.data["flag"] == "train":
                client_model_ptr_dict, server_model_ptr_dict = \
                    message.toDict()["data"]["pointer"], message.toDict()["data"]["call_back_pointer"]

                client_model = DataWarehouse().get(client_model_ptr_dict["remote_retriever_name"],
                                                   client_model_ptr_dict["remote_id"])
                client_model.load_server(server_model_ptr_dict, message.toDict()["data"]["model"])
                client_model.stepN(X, Y)


            if message.data["id"] == "lr_client_data":
                server_model_ptr_dict, client_model_ptr_dict = \
                    message.toDict()["data"]["pointer"], message.toDict()["data"]["call_back_pointer"]

                server_model = DataWarehouse().get(server_model_ptr_dict["remote_retriever_name"],
                                                   server_model_ptr_dict["remote_id"])
                if server_model:
                    server_model.update_client(client_model_ptr_dict, message.toDict()["data"]["model"])

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Router, cls).__new__(cls)
            cls.instance.communicator = \
                Router._Communicator(ComponentRole.DEFAULT, ADDRESS, PORT_RANGE, LOG_LVL, MASTER_ADDR, RL_ADDR)

        return cls.instance
