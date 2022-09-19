from threading import Thread

from federated_learning.federaed_learning_model.synchronous_linear_regression import linear_regression
from federated_learning.federaed_learning_model.base import base_model


from federated_learning.federaed_learning_model.datawarehouse import model_warehouse
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
    model = linear_regression()
    for i in range(10):
        model.add_client(addr, (i+1, 1))
    while (len(model.client) + len(model.server) + len(model.peer)) < 10:
        time.sleep(0.01)

    m = model_warehouse()

    for i in range(10):
        print(i)
        for cli in model.get_client():
            if model.eligible_client(cli):
                model.step_client(cli, 50)

        while not model.can_federate():
            time.sleep(0.01)
        model.federate()
        time.sleep(3) # time until next round

    time.sleep(5)
    print("------------------model_info")
    print(model.dummy_content)
    print("------------------model_param")
    print(model.lr.linear.weight.data)
    print(model.lr.linear.bias.data)
    print(123)
    """
    print("8dc5b218-3838-11ed-8fe3-001c425a9bb9 0 created at Mon Sep 19 16:31:46 2022\n8dc5b218-3838-11ed-8fe3-001c425a9bb9 0 start_fl at Mon Sep 19 16:31:46 2022\nLoad client 4: (('10.211.55.43', 54321), '8db61bbe-3838-11ed-adb8-001c429d7efc')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8db61bbe-3838-11ed-adb8-001c429d7efc_50.txt', 50, 0)\nLoad client 5: (('10.211.55.43', 54321), '8db68234-3838-11ed-b0de-001c429d7efc')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8db68234-3838-11ed-b0de-001c429d7efc_50.txt', 50, 0)\nLoad client 0: (('10.211.55.42', 54322), '8da75642-3838-11ed-b978-001c42f40f40')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8da75642-3838-11ed-b978-001c42f40f40_50.txt', 50, 0)\nLoad client 7: (('10.211.55.44', 54323), '8dd1a9ce-3838-11ed-9506-001c4296df4f')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8dd1a9ce-3838-11ed-9506-001c4296df4f_50.txt', 50, 0)\nLoad client 6: (('10.211.55.44', 54323), '8dd16072-3838-11ed-8ac4-001c4296df4f')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8dd16072-3838-11ed-8ac4-001c4296df4f_50.txt', 50, 0)\nLoad client 3: (('10.211.55.43', 54321), '8db5d71c-3838-11ed-a876-001c429d7efc')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8db5d71c-3838-11ed-a876-001c429d7efc_50.txt', 50, 0)\nLoad client 1: (('10.211.55.42', 54322), '8da77f0a-3838-11ed-85c9-001c42f40f40')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8da77f0a-3838-11ed-85c9-001c42f40f40_50.txt', 50, 0)\nLoad client 2: (('10.211.55.42', 54322), '8da7dbd0-3838-11ed-8ad5-001c42f40f40')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8da7dbd0-3838-11ed-8ad5-001c42f40f40_50.txt', 50, 0)\nLoad client 8: (('10.211.55.44', 54323), '8dd23600-3838-11ed-b48a-001c4296df4f')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8dd23600-3838-11ed-b48a-001c4296df4f_50.txt', 50, 0)\n8dc5b218-3838-11ed-8fe3-001c425a9bb9 1 start_fl at Mon Sep 19 16:31:49 2022\nLoad client 4: (('10.211.55.43', 54321), '8db61bbe-3838-11ed-adb8-001c429d7efc')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8db61bbe-3838-11ed-adb8-001c429d7efc_100.txt', 100, 1)\nLoad client 5: (('10.211.55.43', 54321), '8db68234-3838-11ed-b0de-001c429d7efc')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8db68234-3838-11ed-b0de-001c429d7efc_100.txt', 100, 1)\nLoad client 0: (('10.211.55.42', 54322), '8da75642-3838-11ed-b978-001c42f40f40')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8da75642-3838-11ed-b978-001c42f40f40_100.txt', 100, 1)\nLoad client 7: (('10.211.55.44', 54323), '8dd1a9ce-3838-11ed-9506-001c4296df4f')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8dd1a9ce-3838-11ed-9506-001c4296df4f_100.txt', 100, 1)\nLoad client 6: (('10.211.55.44', 54323), '8dd16072-3838-11ed-8ac4-001c4296df4f')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8dd16072-3838-11ed-8ac4-001c4296df4f_100.txt', 100, 1)\nLoad client 3: (('10.211.55.43', 54321), '8db5d71c-3838-11ed-a876-001c429d7efc')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8db5d71c-3838-11ed-a876-001c429d7efc_100.txt', 100, 1)\nLoad client 1: (('10.211.55.42', 54322), '8da77f0a-3838-11ed-85c9-001c42f40f40')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8da77f0a-3838-11ed-85c9-001c42f40f40_100.txt', 100, 1)\nLoad client 2: (('10.211.55.42', 54322), '8da7dbd0-3838-11ed-8ad5-001c42f40f40')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8da7dbd0-3838-11ed-8ad5-001c42f40f40_100.txt', 100, 1)\nLoad client 8: (('10.211.55.44', 54323), '8dd23600-3838-11ed-b48a-001c4296df4f')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8dd23600-3838-11ed-b48a-001c4296df4f_100.txt', 100, 1)\n8dc5b218-3838-11ed-8fe3-001c425a9bb9 2 start_fl at Mon Sep 19 16:31:52 2022\nLoad client 4: (('10.211.55.43', 54321), '8db61bbe-3838-11ed-adb8-001c429d7efc')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8db61bbe-3838-11ed-adb8-001c429d7efc_150.txt', 150, 2)\nLoad client 5: (('10.211.55.43', 54321), '8db68234-3838-11ed-b0de-001c429d7efc')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8db68234-3838-11ed-b0de-001c429d7efc_150.txt', 150, 2)\nLoad client 0: (('10.211.55.42', 54322), '8da75642-3838-11ed-b978-001c42f40f40')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8da75642-3838-11ed-b978-001c42f40f40_150.txt', 150, 2)\nLoad client 7: (('10.211.55.44', 54323), '8dd1a9ce-3838-11ed-9506-001c4296df4f')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8dd1a9ce-3838-11ed-9506-001c4296df4f_150.txt', 150, 2)\nLoad client 6: (('10.211.55.44', 54323), '8dd16072-3838-11ed-8ac4-001c4296df4f')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8dd16072-3838-11ed-8ac4-001c4296df4f_150.txt', 150, 2)\nLoad client 3: (('10.211.55.43', 54321), '8db5d71c-3838-11ed-a876-001c429d7efc')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8db5d71c-3838-11ed-a876-001c429d7efc_150.txt', 150, 2)\nLoad client 1: (('10.211.55.42', 54322), '8da77f0a-3838-11ed-85c9-001c42f40f40')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8da77f0a-3838-11ed-85c9-001c42f40f40_150.txt', 150, 2)\nLoad client 2: (('10.211.55.42', 54322), '8da7dbd0-3838-11ed-8ad5-001c42f40f40')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8da7dbd0-3838-11ed-8ad5-001c42f40f40_150.txt', 150, 2)\nLoad client 8: (('10.211.55.44', 54323), '8dd23600-3838-11ed-b48a-001c4296df4f')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8dd23600-3838-11ed-b48a-001c4296df4f_150.txt', 150, 2)\n8dc5b218-3838-11ed-8fe3-001c425a9bb9 3 start_fl at Mon Sep 19 16:31:55 2022\nLoad client 4: (('10.211.55.43', 54321), '8db61bbe-3838-11ed-adb8-001c429d7efc')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8db61bbe-3838-11ed-adb8-001c429d7efc_200.txt', 200, 3)\nLoad client 5: (('10.211.55.43', 54321), '8db68234-3838-11ed-b0de-001c429d7efc')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8db68234-3838-11ed-b0de-001c429d7efc_200.txt', 200, 3)\nLoad client 0: (('10.211.55.42', 54322), '8da75642-3838-11ed-b978-001c42f40f40')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8da75642-3838-11ed-b978-001c42f40f40_200.txt', 200, 3)\nLoad client 7: (('10.211.55.44', 54323), '8dd1a9ce-3838-11ed-9506-001c4296df4f')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8dd1a9ce-3838-11ed-9506-001c4296df4f_200.txt', 200, 3)\nLoad client 6: (('10.211.55.44', 54323), '8dd16072-3838-11ed-8ac4-001c4296df4f')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8dd16072-3838-11ed-8ac4-001c4296df4f_200.txt', 200, 3)\nLoad client 3: (('10.211.55.43', 54321), '8db5d71c-3838-11ed-a876-001c429d7efc')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8db5d71c-3838-11ed-a876-001c429d7efc_200.txt', 200, 3)\nLoad client 1: (('10.211.55.42', 54322), '8da77f0a-3838-11ed-85c9-001c42f40f40')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8da77f0a-3838-11ed-85c9-001c42f40f40_200.txt', 200, 3)\nLoad client 2: (('10.211.55.42', 54322), '8da7dbd0-3838-11ed-8ad5-001c42f40f40')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8da7dbd0-3838-11ed-8ad5-001c42f40f40_200.txt', 200, 3)\nLoad client 8: (('10.211.55.44', 54323), '8dd23600-3838-11ed-b48a-001c4296df4f')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8dd23600-3838-11ed-b48a-001c4296df4f_200.txt', 200, 3)\n8dc5b218-3838-11ed-8fe3-001c425a9bb9 4 start_fl at Mon Sep 19 16:31:59 2022\nLoad client 4: (('10.211.55.43', 54321), '8db61bbe-3838-11ed-adb8-001c429d7efc')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8db61bbe-3838-11ed-adb8-001c429d7efc_250.txt', 250, 4)\nLoad client 0: (('10.211.55.42', 54322), '8da75642-3838-11ed-b978-001c42f40f40')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8da75642-3838-11ed-b978-001c42f40f40_250.txt', 250, 4)\nLoad client 7: (('10.211.55.44', 54323), '8dd1a9ce-3838-11ed-9506-001c4296df4f')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8dd1a9ce-3838-11ed-9506-001c4296df4f_250.txt', 250, 4)\nLoad client 3: (('10.211.55.43', 54321), '8db5d71c-3838-11ed-a876-001c429d7efc')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8db5d71c-3838-11ed-a876-001c429d7efc_250.txt', 250, 4)\nLoad client 2: (('10.211.55.42', 54322), '8da7dbd0-3838-11ed-8ad5-001c42f40f40')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8da7dbd0-3838-11ed-8ad5-001c42f40f40_250.txt', 250, 4)\nLoad client 8: (('10.211.55.44', 54323), '8dd23600-3838-11ed-b48a-001c4296df4f')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8dd23600-3838-11ed-b48a-001c4296df4f_250.txt', 250, 4)\n8dc5b218-3838-11ed-8fe3-001c425a9bb9 5 start_fl at Mon Sep 19 16:32:02 2022\nLoad client 5: (('10.211.55.43', 54321), '8db68234-3838-11ed-b0de-001c429d7efc')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8db68234-3838-11ed-b0de-001c429d7efc_300.txt', 300, 5)\nLoad client 7: (('10.211.55.44', 54323), '8dd1a9ce-3838-11ed-9506-001c4296df4f')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8dd1a9ce-3838-11ed-9506-001c4296df4f_300.txt', 300, 5)\nLoad client 6: (('10.211.55.44', 54323), '8dd16072-3838-11ed-8ac4-001c4296df4f')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8dd16072-3838-11ed-8ac4-001c4296df4f_300.txt', 300, 5)\nLoad client 1: (('10.211.55.42', 54322), '8da77f0a-3838-11ed-85c9-001c42f40f40')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8da77f0a-3838-11ed-85c9-001c42f40f40_300.txt', 300, 5)\nLoad client 2: (('10.211.55.42', 54322), '8da7dbd0-3838-11ed-8ad5-001c42f40f40')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8da7dbd0-3838-11ed-8ad5-001c42f40f40_300.txt', 300, 5)\n8dc5b218-3838-11ed-8fe3-001c425a9bb9 6 start_fl at Mon Sep 19 16:32:05 2022\nLoad client 4: (('10.211.55.43', 54321), '8db61bbe-3838-11ed-adb8-001c429d7efc')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8db61bbe-3838-11ed-adb8-001c429d7efc_350.txt', 350, 6)\nLoad client 5: (('10.211.55.43', 54321), '8db68234-3838-11ed-b0de-001c429d7efc')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8db68234-3838-11ed-b0de-001c429d7efc_350.txt', 350, 6)\nLoad client 0: (('10.211.55.42', 54322), '8da75642-3838-11ed-b978-001c42f40f40')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8da75642-3838-11ed-b978-001c42f40f40_350.txt', 350, 6)\nLoad client 7: (('10.211.55.44', 54323), '8dd1a9ce-3838-11ed-9506-001c4296df4f')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8dd1a9ce-3838-11ed-9506-001c4296df4f_350.txt', 350, 6)\nLoad client 6: (('10.211.55.44', 54323), '8dd16072-3838-11ed-8ac4-001c4296df4f')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8dd16072-3838-11ed-8ac4-001c4296df4f_350.txt', 350, 6)\nLoad client 3: (('10.211.55.43', 54321), '8db5d71c-3838-11ed-a876-001c429d7efc')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8db5d71c-3838-11ed-a876-001c429d7efc_350.txt', 350, 6)\nLoad client 1: (('10.211.55.42', 54322), '8da77f0a-3838-11ed-85c9-001c42f40f40')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8da77f0a-3838-11ed-85c9-001c42f40f40_350.txt', 350, 6)\nLoad client 2: (('10.211.55.42', 54322), '8da7dbd0-3838-11ed-8ad5-001c42f40f40')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8da7dbd0-3838-11ed-8ad5-001c42f40f40_350.txt', 350, 6)\nLoad client 8: (('10.211.55.44', 54323), '8dd23600-3838-11ed-b48a-001c4296df4f')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8dd23600-3838-11ed-b48a-001c4296df4f_350.txt', 350, 6)\n8dc5b218-3838-11ed-8fe3-001c425a9bb9 7 start_fl at Mon Sep 19 16:32:08 2022\nLoad client 4: (('10.211.55.43', 54321), '8db61bbe-3838-11ed-adb8-001c429d7efc')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8db61bbe-3838-11ed-adb8-001c429d7efc_400.txt', 400, 7)\nLoad client 5: (('10.211.55.43', 54321), '8db68234-3838-11ed-b0de-001c429d7efc')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8db68234-3838-11ed-b0de-001c429d7efc_400.txt', 400, 7)\nLoad client 0: (('10.211.55.42', 54322), '8da75642-3838-11ed-b978-001c42f40f40')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8da75642-3838-11ed-b978-001c42f40f40_400.txt', 400, 7)\nLoad client 7: (('10.211.55.44', 54323), '8dd1a9ce-3838-11ed-9506-001c4296df4f')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8dd1a9ce-3838-11ed-9506-001c4296df4f_400.txt', 400, 7)\nLoad client 6: (('10.211.55.44', 54323), '8dd16072-3838-11ed-8ac4-001c4296df4f')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8dd16072-3838-11ed-8ac4-001c4296df4f_400.txt', 400, 7)\nLoad client 3: (('10.211.55.43', 54321), '8db5d71c-3838-11ed-a876-001c429d7efc')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8db5d71c-3838-11ed-a876-001c429d7efc_400.txt', 400, 7)\nLoad client 1: (('10.211.55.42', 54322), '8da77f0a-3838-11ed-85c9-001c42f40f40')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8da77f0a-3838-11ed-85c9-001c42f40f40_400.txt', 400, 7)\nLoad client 2: (('10.211.55.42', 54322), '8da7dbd0-3838-11ed-8ad5-001c42f40f40')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8da7dbd0-3838-11ed-8ad5-001c42f40f40_400.txt', 400, 7)\nLoad client 8: (('10.211.55.44', 54323), '8dd23600-3838-11ed-b48a-001c4296df4f')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8dd23600-3838-11ed-b48a-001c4296df4f_400.txt', 400, 7)\n8dc5b218-3838-11ed-8fe3-001c425a9bb9 8 start_fl at Mon Sep 19 16:32:11 2022\nLoad client 4: (('10.211.55.43', 54321), '8db61bbe-3838-11ed-adb8-001c429d7efc')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8db61bbe-3838-11ed-adb8-001c429d7efc_450.txt', 450, 8)\nLoad client 5: (('10.211.55.43', 54321), '8db68234-3838-11ed-b0de-001c429d7efc')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8db68234-3838-11ed-b0de-001c429d7efc_450.txt', 450, 8)\nLoad client 0: (('10.211.55.42', 54322), '8da75642-3838-11ed-b978-001c42f40f40')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8da75642-3838-11ed-b978-001c42f40f40_450.txt', 450, 8)\nLoad client 7: (('10.211.55.44', 54323), '8dd1a9ce-3838-11ed-9506-001c4296df4f')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8dd1a9ce-3838-11ed-9506-001c4296df4f_450.txt', 450, 8)\nLoad client 6: (('10.211.55.44', 54323), '8dd16072-3838-11ed-8ac4-001c4296df4f')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8dd16072-3838-11ed-8ac4-001c4296df4f_450.txt', 450, 8)\nLoad client 3: (('10.211.55.43', 54321), '8db5d71c-3838-11ed-a876-001c429d7efc')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8db5d71c-3838-11ed-a876-001c429d7efc_450.txt', 450, 8)\nLoad client 1: (('10.211.55.42', 54322), '8da77f0a-3838-11ed-85c9-001c42f40f40')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8da77f0a-3838-11ed-85c9-001c42f40f40_450.txt', 450, 8)\nLoad client 2: (('10.211.55.42', 54322), '8da7dbd0-3838-11ed-8ad5-001c42f40f40')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8da7dbd0-3838-11ed-8ad5-001c42f40f40_450.txt', 450, 8)\nLoad client 8: (('10.211.55.44', 54323), '8dd23600-3838-11ed-b48a-001c4296df4f')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8dd23600-3838-11ed-b48a-001c4296df4f_450.txt', 450, 8)\n8dc5b218-3838-11ed-8fe3-001c425a9bb9 9 start_fl at Mon Sep 19 16:32:14 2022\nLoad client 4: (('10.211.55.43', 54321), '8db61bbe-3838-11ed-adb8-001c429d7efc')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8db61bbe-3838-11ed-adb8-001c429d7efc_500.txt', 500, 9)\nLoad client 5: (('10.211.55.43', 54321), '8db68234-3838-11ed-b0de-001c429d7efc')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8db68234-3838-11ed-b0de-001c429d7efc_500.txt', 500, 9)\nLoad client 0: (('10.211.55.42', 54322), '8da75642-3838-11ed-b978-001c42f40f40')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8da75642-3838-11ed-b978-001c42f40f40_500.txt', 500, 9)\nLoad client 7: (('10.211.55.44', 54323), '8dd1a9ce-3838-11ed-9506-001c4296df4f')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8dd1a9ce-3838-11ed-9506-001c4296df4f_500.txt', 500, 9)\nLoad client 6: (('10.211.55.44', 54323), '8dd16072-3838-11ed-8ac4-001c4296df4f')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8dd16072-3838-11ed-8ac4-001c4296df4f_500.txt', 500, 9)\nLoad client 3: (('10.211.55.43', 54321), '8db5d71c-3838-11ed-a876-001c429d7efc')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8db5d71c-3838-11ed-a876-001c429d7efc_500.txt', 500, 9)\nLoad client 1: (('10.211.55.42', 54322), '8da77f0a-3838-11ed-85c9-001c42f40f40')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8da77f0a-3838-11ed-85c9-001c42f40f40_500.txt', 500, 9)\nLoad client 2: (('10.211.55.42', 54322), '8da7dbd0-3838-11ed-8ad5-001c42f40f40')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8da7dbd0-3838-11ed-8ad5-001c42f40f40_500.txt', 500, 9)\nLoad client 8: (('10.211.55.44', 54323), '8dd23600-3838-11ed-b48a-001c4296df4f')with credential ('/workplace/utils/taskExecutor/tasks/federated_learning/communicate/tmp/8dc5b218-3838-11ed-8fe3-001c425a9bb9_c_8dd23600-3838-11ed-b48a-001c4296df4f_500.txt', 500, 9)\n")
