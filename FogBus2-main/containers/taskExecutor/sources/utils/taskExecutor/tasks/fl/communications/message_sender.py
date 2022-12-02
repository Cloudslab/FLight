"""
Sending message to message receiver on other nodes, the reason that use TPC instead of UDP is:
1. The framework is not that performance aware (few sec delay between message is fine)
2. Ref: https://stackoverflow.com/questions/47903/udp-vs-tcp-how-much-faster-is-it Through put control
3. Model communication which is the most communication consuming tasks does not pass through this module
(FTP of warehouse instead)
4. Reliability
"""


import queue
import socket
import pickle
from threading import Thread
from .handlers.abstract_handler import abstract_handler
ADDR_LEN = 40
HANDLER_NAME_LENGTH = abstract_handler.HANDLER_NAME_LENGTH


class message_sender:
    def __init__(self, default_reply_address=""):
        self._sending_queue = queue.Queue()
        self._default_reply_address = default_reply_address

    def _send(self):

        while True:
            address, event, data, reply_address = self._sending_queue.get()
            if not reply_address:
                reply_address = self._default_reply_address
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(address)
                s.sendall(event.encode('utf-8') + reply_address.encode("utf-8").ljust(ADDR_LEN) + pickle.dumps(data))
            except Exception as e:
                print(e)

    def send(self, address, event, data, reply_address=None):
        event = event.ljust(HANDLER_NAME_LENGTH)[:HANDLER_NAME_LENGTH]
        self._sending_queue.put((address, event, data, reply_address))

    def start(self):
        Thread(target=self._send, args=()).start()
