from .base import BaseTask

from .federated_learning.communicate.router import router_factory, ftp_server_factory

from .federated_learning.handler.relationship_handler import relationship_handler
from .federated_learning.handler.model_communication_handler import model_communication_handler
from .federated_learning.handler.remote_call_handler import remote_call_handler

class federatedLearning0(BaseTask):
    def __init__(self):
        super().__init__(taskID=231, taskName='FederatedLearning0')

    def exec(self, inputData):

        addr, r = router_factory.get_router(inputData["self_addr"])
        ftp_server_factory.set_ftp_server(inputData["self_addr"])
        r.add_handler("relation__", relationship_handler())
        r.add_handler("communicat", model_communication_handler())
        r.add_handler("cli_step__", remote_call_handler())

        return addr
