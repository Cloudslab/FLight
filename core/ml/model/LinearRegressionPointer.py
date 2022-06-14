from ..Pointer import Pointer
from ...communication.utils.types import Address
from ...warehouse.ModelWarehouse import ModelRetriever
from ...communication.message.LinearRegressionPointerMessages import LinearRegressionAckMessage
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

    # used for linear regression client to to tell remote server local model is ready
    def ack_client_ready(self, client_ptr: Pointer):
        message_to_send = LinearRegressionAckMessage(self, client_ptr)
        Router().communicator.sendMessage(message_to_send)