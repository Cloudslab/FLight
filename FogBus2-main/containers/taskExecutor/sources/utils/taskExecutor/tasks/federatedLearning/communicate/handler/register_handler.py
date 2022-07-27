from .base_handler import base_handler
import pickle

class register_handler(base_handler):

    def __call__(self, conn, addr, tunnel):

        if conn.recv(3) == b"LR_":
            print(pickle.loads(conn.recv(1024)))