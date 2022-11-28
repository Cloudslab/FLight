from fl.warehouse.warehouse import warehouse

if __name__ == "__main__":
    print("Test Starts")

    # Unit Tests
    print("========= Unit Tests =========")

    # Data warehouse & model warehouse unit test
    print("========= Warehouse Unit Tests =========")

    # -----------------------------------------------------
    print("========= Test 1 Insert to RAM START=========")
    model = {1: 1, 2: 2}
    data = {"x": [1], "y": [1]}
    w = warehouse()
    data_id = warehouse().set_data(data)
    model_id = warehouse().set_model(model)

    print("========= Test 1 Insert to RAM END===========")

    # -----------------------------------------------------
    print("========= Test 2 Retrieve from RAM START=========")
    data_back = warehouse().get_data(data_id)
    model_back = warehouse().get_model(model_id)
    assert data_back == data
    assert model_back == model
    print("========= Test 2 Retrieve from RAM END=========")

    # -----------------------------------------------------
    print("========= Test 3 Retrieve not exist START=========")
    data_not_exist = warehouse().get_data(data_id+"_")
    model_not_exist = warehouse().get_model(model_id + "_")
    assert data_not_exist is None
    assert model_not_exist is None
    print("========= Test 3 Retrieve not exist END=========")