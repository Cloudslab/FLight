"""
Points to a remote object
"""


from abc import ABC, abstractmethod
from ..communication.utils.types import MessageSubType, MessageSubSubType, Address
from ..communication.message import PointerMessage, PointerMessage_RETRIEVE, PointerDataMessage
from ..communication.routing import Router
from ..warehouse.DataWarehouse import DataWarehouse


class Pointer(ABC):
    __slots__ = ["address", "remote_id", "version", "remote_retriever_name"]

    def __init__(self, address: Address, remote_id: int, version: int, remote_retriever_name: str):
        self.address = address
        self.remote_id = remote_id
        self.version = version
        self.remote_retriever_name = remote_retriever_name

    # provide this pointer and send to remote
    def export_pointer(self, remote_address: Address):
        message_to_send = PointerMessage(self, remote_address)
        Router().communicator.sendMessage(message_to_send)

    # Fetch remote data given this pointer
    def retrieve(self, call_back_pointer: 'Pointer'):
        message_to_send = PointerMessage_RETRIEVE(self, call_back_pointer)
        Router().communicator.sendMessage(message_to_send)

    # given the pointer
    def export_data(self, call_back_pointer: 'Pointer'):
        data = DataWarehouse().get(self.remote_retriever_name, self.remote_id)
        message_to_send = PointerDataMessage(data, call_back_pointer)
        Router().communicator.sendMessage(message_to_send)
