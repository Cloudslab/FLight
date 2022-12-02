"""
Class that receives message and dispatch to an appropriate message handler
"""

import socket
import ast
from threading import Thread
from .message_sender import ADDR_LEN
from .handlers.abstract_handler import abstract_handler
from .handlers.handler_manager import handler_manager
event_string_len = abstract_handler.HANDLER_NAME_LENGTH


class message_receiver:
    def __init__(self, address, listen_amount = 10):
        self._socket = None
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind(address)
        self._listen_amount = listen_amount

    def __del__(self):
        if self._socket:
            self._socket.close()

    def _dispatch(self):
        self._socket.listen(self._listen_amount)
        while True:
            conn, _ = self._socket.accept()
            event = conn.recv(event_string_len).decode('utf-8')
            reply_address = ast.literal_eval(conn.recv(ADDR_LEN).decode("utf-8").rstrip())
            corresponding_handler = handler_manager.get_handler(event)
            if corresponding_handler:
                Thread(target=corresponding_handler, args=(conn, reply_address, )).start()
            else:
                x = 1
                x.sot()

    def start(self):
        Thread(target=self._dispatch, args=()).start()
