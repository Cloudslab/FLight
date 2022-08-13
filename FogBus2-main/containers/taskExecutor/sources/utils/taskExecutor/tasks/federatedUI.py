import random

from federated_learning.federaed_learning_model.datawarehouse import data_warehouse


def scale(x_data, y_data):
    if x_data == 0 and y_data == 0:
        return x_data, y_data

    m = max(abs(x), abs(y)) * (random.random()*0.1 + 0.9)
    return x_data/m, y_data/m


while True:
    print(""
          "[i] input data\n"
          "[x] clear data\n"
          "[s] show data\n"
          "[e] exit"
          "")
    print ("Selection: ", end="")
    k = input()

    if k == "i":
        print("x: ", end="")
        x = float(input())
        print("y: ", end="")
        y = float(input())

        data_warehouse.insert_xy(x, y)
    elif k == "x":
        data_warehouse.clear()

    elif k == "s":
        print(data_warehouse.read_from_database("xy"))
    elif k == "e":
        break