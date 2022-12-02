"""Handler to handle relationships"""
from .abstract_handler import abstract_handler
from ...warehouse.warehouse import warehouse
import pickle
from enum import Enum

class relationship_handler(abstract_handler):
    name = "relat"

    class sub_events(Enum):
        add_client = 1
        add_server = 2
        add_peer = 3
        ack_add = 4

    def __call__(self, conn, reply_addr, *args, **kwargs):
        data_received = pickle.loads((conn.recv(2048)))
        id_back = warehouse().set_data(data={"raw_data": data_received,"file_name": "data_received.txt"}, data_id=None,
                                       storage="local_file")

    def __init__(self):
        pass
