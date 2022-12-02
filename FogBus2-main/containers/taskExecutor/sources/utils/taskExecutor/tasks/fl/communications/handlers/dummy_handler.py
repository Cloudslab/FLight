"""Sample dummy handler"""
from .abstract_handler import abstract_handler
import pickle


class dummy_handler(abstract_handler):
    def __call__(self, conn, reply_addr, *args, **kwargs):
        sub_event = (conn.recv(self.EVENT_STRING_LEN)).decode('utf-8')
        data_received = pickle.loads((conn.recv(2048)))
        print("Received incoming event:\n")
        print(sub_event, data_received)

    def __init__(self):
        self.name = "dummy"
