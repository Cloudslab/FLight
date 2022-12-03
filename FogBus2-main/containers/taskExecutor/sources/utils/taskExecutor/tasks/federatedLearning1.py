from .base import BaseTask

from .federated_learning.communicate.router import router_factory, ftp_server_factory

from .federated_learning.handler.relationship_handler import relationship_handler
from .federated_learning.handler.model_communication_handler import model_communication_handler
from .federated_learning.handler.remote_call_handler import remote_call_handler



# ------------------------ import from new version
from .fl.communications.router import router
from .fl.warehouse.warehouse import warehouse


class federatedLearning1(BaseTask):
    def __init__(self):
        super().__init__(taskID=232, taskName='FederatedLearning1')

    def exec(self, inputData):

        router(inputData["self_addr"])
        warehouse().model_warehouse.start_ftp_server(inputData["self_addr"])
        addr = router.get_default_router().message_receiver_address
    #    addr, r = router_factory.get_router(inputData["self_addr"])
    #    ftp_server_factory.set_ftp_server(inputData["self_addr"])
    #    r.add_handler("relation__", relationship_handler())
    #    r.add_handler("communicat", model_communication_handler())
    #    r.add_handler("cli_step__", remote_call_handler())

        return addr
