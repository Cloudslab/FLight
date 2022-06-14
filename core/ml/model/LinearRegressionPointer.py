from ..Pointer import Pointer
from ...communication.message import PointerMessage
from ...communication.utils.types import Address
from ...warehouse.ModelWarehouse import ModelRetriever
from ...communication.message.LinearRegressionPointerMessages import LinearRegressionAckMessage, LinearRegressionStep, \
    LinearRegressionFetchServer, LinearRegressionServerData, LinearRegressionClientData
from ...communication.routing import Router

class LinearRegressionPointer(Pointer):

    def __init__(self, linear_regression_model: 'LinearRegression', address: Address, unique_id: int):
        version = \
            linear_regression_model if isinstance(linear_regression_model, int) else linear_regression_model.version
        super().__init__(address, unique_id, version, ModelRetriever.RETRIEVER_NAMESPACE)

    @classmethod
    def fromDict(cls, d: dict):
        if "version" in d and "remote_id" in d and "address" in d:
            return LinearRegressionPointer(d["version"], d["address"], d["remote_id"])

        else:
            # ToDo log error here
            return None

    def export_pointer(self, remote_address: Address):
        message_to_send = PointerMessage(self, remote_address, "lr_init")
        Router().communicator.sendMessage(message_to_send)

    # when a server pointer is hold by client, client can use it to tell remote server local model is ready
    def ack_client_ready(self, client_ptr: Pointer):
        message_to_send = LinearRegressionAckMessage(self, client_ptr)
        Router().communicator.sendMessage(message_to_send)

    # when a client pointer is hold by server, server can use it to invite client to do a train
    def step(self, server_ptr: Pointer):
        message_to_send = LinearRegressionStep(self, server_ptr)
        Router().communicator.sendMessage(message_to_send)

    # when a server pointer is hold by client, client can use it to fetch server data
    def fetch_server(self, client_ptr: Pointer):
        message_to_send = LinearRegressionFetchServer(self, client_ptr)
        Router().communicator.sendMessage(message_to_send)

    # when a client pointer is hold by server, server can use it to push local data to client (indicate if just give or
    # ask to train)
    def push_client(self, server_ptr: Pointer, model_data: dict, flag: str):
        message_to_send = LinearRegressionServerData(self, server_ptr, model_data, flag)
        Router().communicator.sendMessage(message_to_send)

    # when a server pointer is hold by client, client can use it to push local data to server (indicate if just give or
    # ask to train)
    def push_server(self, client_ptr: Pointer, model_data: dict, flag: str):
        message_to_send = LinearRegressionClientData(self, client_ptr, model_data, flag)
        Router().communicator.sendMessage(message_to_send)
