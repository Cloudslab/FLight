import socket
import struct
import pickle
if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("127.0.0.1", 12345))
        buf = b"register"
        buf += b"LR_"
        numbers = [12434.01223, 21031.313943]

        buf += pickle.dumps(numbers)
        s.sendall(buf)
        #do = [12.43, 12.442, 1234.433]

        #s.sendall(do)
