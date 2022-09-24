from threading import Thread

from federated_learning.federaed_learning_model.synchronous_linear_regression import linear_regression
from federated_learning.federaed_learning_model.base import base_model
from federated_learning.federaed_learning_model.synchronous_cv import synchronous_computer_vision

from federated_learning.federaed_learning_model.datawarehouse import model_warehouse, data_warehouse
from federated_learning.communicate.router import router_factory, ftp_server_factory
from federated_learning.handler.relationship_handler import relationship_handler
from federated_learning.handler.model_communication_handler import model_communication_handler
from federated_learning.handler.remote_call_handler import remote_call_handler

import time

import glob

if __name__ == "__main__":
    """
    addr, r = router_factory.get_router(("127.0.0.1", 12345))
    ftp_addr, ftp_server = ftp_server_factory.get_ftp_server(("127.0.0.1", 12345))
    r.add_handler("relation__", relationship_handler())
    r.add_handler("communicat", model_communication_handler())
    r.add_handler("cli_step__", remote_call_handler())
    model = synchronous_computer_vision(0)
    for i in range(10):
        model.add_client(addr, i)
    while (len(model.client) + len(model.server) + len(model.peer)) < 10:
        time.sleep(0.01)

    m = model_warehouse()

    for i in range(10):
        print(i)
        for cli in model.get_client():
            if model.eligible_client(cli):
                model.step_client(cli, 20)

        while not model.can_federate():
            time.sleep(0.01)
        model.federate()
        print("Average Accuracy: {}", model.cv1.accuracy)
        time.sleep(3) # time until next round
    print(model.dummy_content)
    print("Done")
    # time.sleep(5)
    # print("------------------model_info")
    # print(model.dummy_content)
    # print("------------------model_param")
    # print(model.lr.linear.weight.data)
    # print(model.lr.linear.bias.data)
    """
    print("d369615c-38d8-11ed-b3f4-001c42f40f40 0 created at Tue Sep 20 11:39:02 2022\nd369615c-38d8-11ed-b3f4-001c42f40f40 0 start_fl at Tue Sep 20 11:39:07 2022\nLoad client 0: (('10.211.55.43', 54323), 'd35dd3be-38d8-11ed-a0b1-001c429d7efc')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/d369615c-38d8-11ed-b3f4-001c42f40f40_c_d35dd3be-38d8-11ed-a0b1-001c429d7efc_20.txt', 20, 0)\nLoad client 1: (('10.211.55.43', 54323), 'd35dfb3c-38d8-11ed-9bd3-001c429d7efc')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/d369615c-38d8-11ed-b3f4-001c42f40f40_c_d35dfb3c-38d8-11ed-9bd3-001c429d7efc_20.txt', 20, 0)\nLoad client 7: (('10.211.55.45', 54322), 'd380883c-38d8-11ed-9f7e-001c425a9bb9')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/d369615c-38d8-11ed-b3f4-001c42f40f40_c_d380883c-38d8-11ed-9f7e-001c425a9bb9_20.txt', 20, 0)\nAchieve average accuracy of tensor(13.8542)\nd369615c-38d8-11ed-b3f4-001c42f40f40 1 start_fl at Tue Sep 20 11:39:15 2022\nLoad client 0: (('10.211.55.43', 54323), 'd35dd3be-38d8-11ed-a0b1-001c429d7efc')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/d369615c-38d8-11ed-b3f4-001c42f40f40_c_d35dd3be-38d8-11ed-a0b1-001c429d7efc_40.txt', 40, 1)\nLoad client 1: (('10.211.55.43', 54323), 'd35dfb3c-38d8-11ed-9bd3-001c429d7efc')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/d369615c-38d8-11ed-b3f4-001c42f40f40_c_d35dfb3c-38d8-11ed-9bd3-001c429d7efc_40.txt', 40, 1)\nLoad client 2: (('10.211.55.43', 54323), 'd35e05c8-38d8-11ed-95db-001c429d7efc')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/d369615c-38d8-11ed-b3f4-001c42f40f40_c_d35e05c8-38d8-11ed-95db-001c429d7efc_40.txt', 40, 1)\nAchieve average accuracy of tensor(23.7760)\nd369615c-38d8-11ed-b3f4-001c42f40f40 2 start_fl at Tue Sep 20 11:39:23 2022\nLoad client 7: (('10.211.55.45', 54322), 'd380883c-38d8-11ed-9f7e-001c425a9bb9')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/d369615c-38d8-11ed-b3f4-001c42f40f40_c_d380883c-38d8-11ed-9f7e-001c425a9bb9_60.txt', 60, 2)\nLoad client 2: (('10.211.55.43', 54323), 'd35e05c8-38d8-11ed-95db-001c429d7efc')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/d369615c-38d8-11ed-b3f4-001c42f40f40_c_d35e05c8-38d8-11ed-95db-001c429d7efc_60.txt', 60, 2)\nLoad client 8: (('10.211.55.45', 54322), 'd3809340-38d8-11ed-8bb3-001c425a9bb9')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/d369615c-38d8-11ed-b3f4-001c42f40f40_c_d3809340-38d8-11ed-8bb3-001c425a9bb9_60.txt', 60, 2)\nAchieve average accuracy of tensor(38.0729)\nd369615c-38d8-11ed-b3f4-001c42f40f40 3 start_fl at Tue Sep 20 11:39:30 2022\nLoad client 0: (('10.211.55.43', 54323), 'd35dd3be-38d8-11ed-a0b1-001c429d7efc')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/d369615c-38d8-11ed-b3f4-001c42f40f40_c_d35dd3be-38d8-11ed-a0b1-001c429d7efc_80.txt', 80, 3)\nLoad client 1: (('10.211.55.43', 54323), 'd35dfb3c-38d8-11ed-9bd3-001c429d7efc')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/d369615c-38d8-11ed-b3f4-001c42f40f40_c_d35dfb3c-38d8-11ed-9bd3-001c429d7efc_80.txt', 80, 3)\nLoad client 2: (('10.211.55.43', 54323), 'd35e05c8-38d8-11ed-95db-001c429d7efc')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/d369615c-38d8-11ed-b3f4-001c42f40f40_c_d35e05c8-38d8-11ed-95db-001c429d7efc_80.txt', 80, 3)\nAchieve average accuracy of tensor(60.9896)\nd369615c-38d8-11ed-b3f4-001c42f40f40 4 start_fl at Tue Sep 20 11:39:38 2022\nLoad client 7: (('10.211.55.45', 54322), 'd380883c-38d8-11ed-9f7e-001c425a9bb9')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/d369615c-38d8-11ed-b3f4-001c42f40f40_c_d380883c-38d8-11ed-9f7e-001c425a9bb9_100.txt', 100, 4)\nLoad client 2: (('10.211.55.43', 54323), 'd35e05c8-38d8-11ed-95db-001c429d7efc')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/d369615c-38d8-11ed-b3f4-001c42f40f40_c_d35e05c8-38d8-11ed-95db-001c429d7efc_100.txt', 100, 4)\nLoad client 8: (('10.211.55.45', 54322), 'd3809340-38d8-11ed-8bb3-001c425a9bb9')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/d369615c-38d8-11ed-b3f4-001c42f40f40_c_d3809340-38d8-11ed-8bb3-001c425a9bb9_100.txt', 100, 4)\nAchieve average accuracy of tensor(67.1875)\nd369615c-38d8-11ed-b3f4-001c42f40f40 5 start_fl at Tue Sep 20 11:39:46 2022\nLoad client 0: (('10.211.55.43', 54323), 'd35dd3be-38d8-11ed-a0b1-001c429d7efc')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/d369615c-38d8-11ed-b3f4-001c42f40f40_c_d35dd3be-38d8-11ed-a0b1-001c429d7efc_120.txt', 120, 5)\nLoad client 1: (('10.211.55.43', 54323), 'd35dfb3c-38d8-11ed-9bd3-001c429d7efc')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/d369615c-38d8-11ed-b3f4-001c42f40f40_c_d35dfb3c-38d8-11ed-9bd3-001c429d7efc_120.txt', 120, 5)\nLoad client 7: (('10.211.55.45', 54322), 'd380883c-38d8-11ed-9f7e-001c425a9bb9')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/d369615c-38d8-11ed-b3f4-001c42f40f40_c_d380883c-38d8-11ed-9f7e-001c425a9bb9_120.txt', 120, 5)\nAchieve average accuracy of tensor(72.6042)\nd369615c-38d8-11ed-b3f4-001c42f40f40 6 start_fl at Tue Sep 20 11:39:54 2022\nLoad client 7: (('10.211.55.45', 54322), 'd380883c-38d8-11ed-9f7e-001c425a9bb9')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/d369615c-38d8-11ed-b3f4-001c42f40f40_c_d380883c-38d8-11ed-9f7e-001c425a9bb9_140.txt', 140, 6)\nLoad client 8: (('10.211.55.45', 54322), 'd3809340-38d8-11ed-8bb3-001c425a9bb9')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/d369615c-38d8-11ed-b3f4-001c42f40f40_c_d3809340-38d8-11ed-8bb3-001c425a9bb9_140.txt', 140, 6)\nLoad client 6: (('10.211.55.45', 54322), 'd3805a06-38d8-11ed-af58-001c425a9bb9')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/d369615c-38d8-11ed-b3f4-001c42f40f40_c_d3805a06-38d8-11ed-af58-001c425a9bb9_140.txt', 140, 6)\nAchieve average accuracy of tensor(74.0885)\nd369615c-38d8-11ed-b3f4-001c42f40f40 7 start_fl at Tue Sep 20 11:40:02 2022\nLoad client 1: (('10.211.55.43', 54323), 'd35dfb3c-38d8-11ed-9bd3-001c429d7efc')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/d369615c-38d8-11ed-b3f4-001c42f40f40_c_d35dfb3c-38d8-11ed-9bd3-001c429d7efc_160.txt', 160, 7)\nLoad client 7: (('10.211.55.45', 54322), 'd380883c-38d8-11ed-9f7e-001c425a9bb9')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/d369615c-38d8-11ed-b3f4-001c42f40f40_c_d380883c-38d8-11ed-9f7e-001c425a9bb9_160.txt', 160, 7)\nLoad client 2: (('10.211.55.43', 54323), 'd35e05c8-38d8-11ed-95db-001c429d7efc')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/d369615c-38d8-11ed-b3f4-001c42f40f40_c_d35e05c8-38d8-11ed-95db-001c429d7efc_160.txt', 160, 7)\nLoad client 6: (('10.211.55.45', 54322), 'd3805a06-38d8-11ed-af58-001c425a9bb9')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/d369615c-38d8-11ed-b3f4-001c42f40f40_c_d3805a06-38d8-11ed-af58-001c425a9bb9_160.txt', 160, 7)\nAchieve average accuracy of tensor(77.1484)\nd369615c-38d8-11ed-b3f4-001c42f40f40 8 start_fl at Tue Sep 20 11:40:10 2022\nLoad client 7: (('10.211.55.45', 54322), 'd380883c-38d8-11ed-9f7e-001c425a9bb9')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/d369615c-38d8-11ed-b3f4-001c42f40f40_c_d380883c-38d8-11ed-9f7e-001c425a9bb9_180.txt', 180, 8)\nLoad client 8: (('10.211.55.45', 54322), 'd3809340-38d8-11ed-8bb3-001c425a9bb9')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/d369615c-38d8-11ed-b3f4-001c42f40f40_c_d3809340-38d8-11ed-8bb3-001c425a9bb9_180.txt', 180, 8)\nLoad client 6: (('10.211.55.45', 54322), 'd3805a06-38d8-11ed-af58-001c425a9bb9')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/d369615c-38d8-11ed-b3f4-001c42f40f40_c_d3805a06-38d8-11ed-af58-001c425a9bb9_180.txt', 180, 8)\nAchieve average accuracy of tensor(76.7448)\nd369615c-38d8-11ed-b3f4-001c42f40f40 9 start_fl at Tue Sep 20 11:40:17 2022\nLoad client 1: (('10.211.55.43', 54323), 'd35dfb3c-38d8-11ed-9bd3-001c429d7efc')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/d369615c-38d8-11ed-b3f4-001c42f40f40_c_d35dfb3c-38d8-11ed-9bd3-001c429d7efc_200.txt', 200, 9)\nLoad client 7: (('10.211.55.45', 54322), 'd380883c-38d8-11ed-9f7e-001c425a9bb9')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/d369615c-38d8-11ed-b3f4-001c42f40f40_c_d380883c-38d8-11ed-9f7e-001c425a9bb9_200.txt', 200, 9)\nLoad client 6: (('10.211.55.45', 54322), 'd3805a06-38d8-11ed-af58-001c425a9bb9')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/d369615c-38d8-11ed-b3f4-001c42f40f40_c_d3805a06-38d8-11ed-af58-001c425a9bb9_200.txt', 200, 9)\nAchieve average accuracy of tensor(78.7240)\n")
    #modell = synchronous_computer_vision(19)
    #i = 1
    #while modell.cv1.accuracy <= 80:
    #    modell.stepp(None)
    #    print(i, modell.cv1.accuracy)

    #print(modell)

