from  federated_learning.federaed_learning_model.base import base_model
from  federated_learning.federaed_learning_model.datawarehouse import model_warehouse
model_handbook = {
    "_bas": base_model
}
if __name__ == "__main__":
    m = model_warehouse()
    id = m.set(1)
    m2 = model_warehouse()
    print(m2.get(id))