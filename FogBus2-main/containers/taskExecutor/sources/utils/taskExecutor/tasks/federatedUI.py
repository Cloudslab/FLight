from federated_learning.federaed_learning_model.datawarehouse import data_warehouse

while True:
    x = input()
    y = input()
    data_warehouse.insert_xy(x, y)