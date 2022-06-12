"""
Points to a remote object
"""
from abc import ABC, abstractmethod
from ..communication.utils.types import MessageSubType, MessageSubSubType, Address
from ..communication.message import PointerMessage
from ..communication.routing import Router

class Pointer(ABC):

    __slots__ = ["address", "remote_id", "version", "remote_retriever_name"]

    def __init__(self, address: Address, remote_id: int, version: int, remote_retriever_name: str):
        self.address = address
        self.remote_id = remote_id
        self.version = version
        self.remote_retriever_name = remote_retriever_name

    # Fetch remote data
    def fetch(self):
        message_to_send = PointerMessage(self, PointerMessage.purpose.RETRIEVE)
        Router().communicator.sendMessage(message_to_send)
