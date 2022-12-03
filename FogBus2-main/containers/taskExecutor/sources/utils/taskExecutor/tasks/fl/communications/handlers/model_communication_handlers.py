"""Handles requests about sending model weights from one site to another"""


from .abstract_handler import abstract_handler
from ...warehouse.warehouse import warehouse
from ...fl_apis.relationship_apis.model_pointer import model_pointer
import pickle
from enum import Enum


class model_communication_handler(abstract_handler):
    name = "comut"

    class sub_event(Enum):
        fetch_model_weights = 1

    def __call__(self, conn, reply_addr, *args, **kwargs):
        pass
