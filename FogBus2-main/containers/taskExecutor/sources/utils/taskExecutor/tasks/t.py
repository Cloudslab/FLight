from fl.warehouse.warehouse import warehouse

if __name__ == "__main__":
    print("Test Starts")

    # Unit Tests
    print("========= Unit Tests =========")

    # Data warehouse & model warehouse unit test
    print("========= Warehouse Unit Tests =========")
    print("========= Test 1 Insert to RAM START=========")
    model = {1:1, 2:2}
    data  = {"x":[1], "y":[1]}
    w = warehouse()
    data_id = warehouse().set_data(data)
    model_id = warehouse().set_model(model)

    print("========= Test 1 Insert to RAM END===========")