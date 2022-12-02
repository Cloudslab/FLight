"""Sample dummy handler"""
from .abstract_handler import abstract_handler
from ...warehouse.warehouse import warehouse
import pickle


class dummy_handler(abstract_handler):
    def __call__(self, conn, reply_addr, *args, **kwargs):
        data_received = pickle.loads((conn.recv(2048)))
        id_back = warehouse().set_data(data={"raw_data": data_received,"file_name": "data_received.txt"}, data_id=None,
                                       storage="local_file")

    def __init__(self):
        self.name = "dummy"  # handler name length is 5
