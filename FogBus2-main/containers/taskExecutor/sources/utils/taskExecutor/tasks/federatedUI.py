from federated_learning.federaed_learning_model.datawarehouse import data_warehouse

while True:
    print(""
          "[i] input data\n"
          "[x] clear data\n"
          "[s] show data"
          "")
    k = input()

    if k == "i":
        x = input()
        y = input()
        data_warehouse.insert_xy(x, y)
    elif k == "x":
        data_warehouse.clear()

    elif k == "s":
        print(data_warehouse.read_from_database("xy"))
