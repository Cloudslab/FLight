from fl.warehouse.warehouse import warehouse
from fl.warehouse.storage_folder.folder_manager import folder_position
from fl.communications.router import router
from fl.fl_apis.base import base
from fl.fl_apis.relationship_apis.model_pointer import model_pointer

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
    router.get_default_router().send(router.get_default_router().message_receiver_address, "dummy", [1, (1, "1")])
    # make sure receive reply on the panel
    print("========= Test 10 Router send Message END=========")

    print("========= Test 11 Establish relationship with remote START=========")
    b = base()
    b.add_server(router.get_default_router().message_receiver_address)
    b.add_client(router.get_default_router().message_receiver_address)
    b.add_peer(router.get_default_router().message_receiver_address)
    import time
    while not b.get_servers() or not b.get_clients() or not b.get_peers():
        time.sleep(0.01)
    remote_server_ptr, remote_client_ptr, remote_peer_ptr = b.get_servers()[0], b.get_clients()[0], b.get_peers()[0]
    remote_server, remote_client, remote_peer = \
        warehouse().get_model(remote_server_ptr.uuid), \
        warehouse().get_model(remote_client_ptr.uuid), \
        warehouse().get_model(remote_peer_ptr.uuid)

    assert remote_server is not None
    assert remote_client is not None
    assert remote_peer is not None
    b_pointer = model_pointer(b.uuid, router.get_default_router().message_receiver_address)
    assert remote_server.get_clients()[0] == b_pointer
    assert remote_client.get_servers()[0] == b_pointer
    assert remote_peer.get_peers()[0] == b_pointer

    print("========= Test 11 Establish relationship with remote END=========")

    print("========= Test 12 Test Request Remote to Train START=========")
    b_server = base()
    b_server.add_client(router.get_default_router().message_receiver_address)
    b_server.add_client(router.get_default_router().message_receiver_address)
    b_server.add_client(router.get_default_router().message_receiver_address)
    while len(b_server.get_clients()) < 3:
        time.sleep(0.01)

    # ----- Train 5 times without evaluate will cause count: 0 += 5
    for client_ptr in b_server.get_clients():
        b_server.train_remote(5, client_ptr)
    time.sleep(1)  # make sure train finished on all clients
    for client_ptr in b_server.get_clients():
        assert warehouse().get_model(client_ptr.uuid).get_model_dict()["count"] == 5
    for version, base_version, credential, additional_args in list(b_server.get_available_remote_model_weights().values()):
        assert base_version == 0
    print(b_server.get_available_remote_model_weights())

    # ----- Train 5 times with evaluate will cause count shift back to original 0 (count from b_server) += 5 = 5
    # ----- Evaluate one time will cause count += 1 (5 + 1 = 6)
    for client_ptr in b_server.get_clients():
        b_server.train_remote(5, client_ptr, evaluate=True)
    time.sleep(1)  # make sure train finished on all clients
    for client_ptr in b_server.get_clients():
        assert warehouse().get_model(client_ptr.uuid).get_model_dict()["count"] == 6
    for v in b_server.get_available_remote_model_weights().values():
        assert v[0] == 10  # experienced 10 trains, so version should be +=5 +=5 = 10
    time.sleep(1)
    # print(b_server.get_available_remote_model_weights())
    print("========= Test 12 Test Request Remote to Train END=========")

    print("========= Test 13 Test Fetch Remote START=========")
    for client_ptr in b_server.get_clients():
        b_server.fetch_remote(client_ptr)
    time.sleep(1)
    assert b_server.can_federate(required_response=["general", 3])  # receive all three response
    assert not b_server.can_federate(required_response=["general", 4])  # receive only three response, less than four required
    print("========= Test 13 Test Fetch Remote END=========")

