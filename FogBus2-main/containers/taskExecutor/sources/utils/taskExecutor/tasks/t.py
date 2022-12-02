from fl.warehouse.warehouse import warehouse
from fl.warehouse.storage_folder.folder_manager import folder_position
from fl.communications.router import router

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
    data_not_exist = warehouse().get_data(data_id + "_")
    model_not_exist = warehouse().get_model(model_id + "_")
    assert data_not_exist is None
    assert model_not_exist is None
    print("========= Test 3 Retrieve not exist END=========")

    # -----------------------------------------------------
    print("======== Test 4 Folder manager START=========")
    local_file_storage_position = folder_position.local_file_storage_folder()
    ftp_file_storage_position = folder_position.ftp_folder()
    # make sure the file path is correct (check by hand...)

    print("======== Test 4 Folder manager END=========")
    # -----------------------------------------------------
    print("======== Test 5 Set & Retrieve from local_file START=========")
    model = {"Test 5 Model": "Version1"}
    data = {"Test 5 Data": {"X": [1], "Y": [2]}}
    data_id = w.set_data({"raw_data": data, "file_name": "test_5_data.txt"}, storage="local_file")
    model_id = w.set_model({"raw_data": model, "file_name": "test_5_model.txt"}, storage="local_file")

    # retrieve
    data_back_from_file = w.get_data(data_id)
    model_back_from_file = w.get_model(model_id)
    assert data_back_from_file == data
    assert model_back_from_file == model
    print("======== Test 5 Set & Retrieve from local_file END=========")

    print("========= Test 6 Retrieve not exist from local_file START=========")
    model_not_exist = warehouse().get_model("ID_NOT_EXIST")
    data_not_exist = warehouse().get_data("ID_NOT_EXIST")
    assert data_not_exist is None
    assert model_not_exist is None
    print("========= Test 6 Retrieve not exist from local_file END=========")

    print("========= Test 7 Set & Retrieve from local_file given ID START=========")
    model_id = "model_id"
    data_id = "data_id"
    data_id_back = w.set_data({"raw_data": data, "file_name": "test_5_data.txt"}, storage="local_file", data_id=data_id)
    model_id_back = w.set_model({"raw_data": model, "file_name": "test_5_model.txt"}, storage="local_file", model_id=model_id)
    assert model_id == model_id_back
    assert data_id == data_id_back

    print("========= Test 7 Set & Retrieve from local_file given ID END=========")

    print("========= Test 8 Saving to FTP server START=========")
    w.model_warehouse.start_ftp_server(addr=("127.0.0.1", 12345))
    model = {"Test 8 Model": "Version1"}
    model_id = w.set_model({"raw_data": model, "file_name": "test_8_model.txt"}, storage="ftp")
    # make sure a file exist in ftp_file_storage
    print("========= Test 8 Saving to FTP server END=========")

    print("========= Test 9 Download from FTP server START=========")
    ftp_server_addr, user_name, password, file_name = w.get_model(model_id)
    assert ftp_server_addr == ("127.0.0.1", 12345)
    w.download_model(ftp_server_addr, file_name, user_name, password)
    # make sure a file downloaded to local_file_storage
    print("========= Test 9 Download from FTP server END=========")

    print("========= Test 10 Router send Message START=========")
    router(("127.0.0.1", 12345))
    from fl.communications.handlers.handler_manager import handler_manager
    router.get_default_router().send(router.get_default_router().message_receiver_address, "dummy", [1, (1, "1")])
    # make sure receive reply on the panel
    print("========= Test 10 Router send Message END=========")
