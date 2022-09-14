from federated_learning.federaed_learning_model.base import base_model
from federated_learning.federaed_learning_model.datawarehouse import model_warehouse
from federated_learning.communicate.router import router_factory
from federated_learning.handler.relationship_handler import relationship_handler
from federated_learning.handler.model_communication_handler import model_communication_handler
import time

model_handbook = {
    "_bas": base_model
}
if __name__ == "__main__":
    #addr, r = router_factory.get_router(("127.0.0.1", 12345))
    #r.add_handler("relation__", relationship_handler())
    #r.add_handler("communicat", model_communication_handler())
    #model = base_model()
    #model.add_client(("127.0.0.1", 12345))
    #model.add_client(("127.0.0.1", 12345))
    #model.add_client(("127.0.0.1", 12345))
    #while len(model.client) < 3:
    #    time.sleep(0.01)

    #print(model.client)
    ptr = 1, 2, 3
    print(ptr)
