from  federated_learning.federaed_learning_model.base import base_model
model_handbook = {
    "_bas": base_model
}
if __name__ == "__main__":
    m = model_handbook["_bas"]()
    m2 = model_handbook["_bas"]()
    print(m.export())
    print(m2.export())