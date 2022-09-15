from threading import Thread

from federated_learning.federaed_learning_model.base import base_model
from federated_learning.federaed_learning_model.datawarehouse import model_warehouse
from federated_learning.communicate.router import router_factory, ftp_server_factory
from federated_learning.handler.relationship_handler import relationship_handler
from federated_learning.handler.model_communication_handler import model_communication_handler

import time

model_handbook = {
    "_bas": base_model
}

import glob

if __name__ == "__main__":
    addr, r = router_factory.get_router(("127.0.0.1", 12345))
    ftp_addr, ftp_server = ftp_server_factory.get_ftp_server(("127.0.0.1", 12345))
    r.add_handler("relation__", relationship_handler())
    r.add_handler("communicat", model_communication_handler())
    model = base_model()
    model.add_server(addr)
    model.add_server(addr)
    model.add_server(addr)
    while (len(model.client) + len(model.server) + len(model.peer)) < 3:
        time.sleep(0.01)
    i = 1
    for cli in model.server:
        model.fetch_server(cli)
    m = model_warehouse()
    print(1234)
    #for cli in model.peer:
    #    m = model_warehouse().get(cli[1])
    #    m.fetch_peer(m.peer[0])
    # print(111)