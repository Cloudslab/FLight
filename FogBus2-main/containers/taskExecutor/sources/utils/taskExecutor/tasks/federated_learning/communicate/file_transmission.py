from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

FTP_PORT = 2121
FTP_USER = "myuser"
FTP_PASSWORD = "change_this_password"
FTP_DIRECTORY = "./tmp/"

if __name__ == "__main__":
    authorizer = DummyAuthorizer()
    authorizer.add_user(FTP_USER, FTP_PASSWORD, FTP_DIRECTORY, perm='elradfmw')
    handler = FTPHandler
    handler.authorizer = authorizer
    address = ('127.0.0.1', FTP_PORT)
    server = FTPServer(address, handler)
    server.serve_forever()
    print(1)

