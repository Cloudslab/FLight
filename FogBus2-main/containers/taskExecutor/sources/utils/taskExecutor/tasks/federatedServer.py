from .base import BaseTask

from .federated_learning.communicate.router import router_factory, ftp_server_factory

from .federated_learning.handler.relationship_handler import relationship_handler
from .federated_learning.federaed_learning_model.base import base_model
from .federated_learning.federaed_learning_model.synchronous_linear_regression import linear_regression
from .federated_learning.federaed_learning_model.synchronous_cv import synchronous_computer_vision
from .federated_learning.handler.model_communication_handler import model_communication_handler
from .federated_learning.handler.remote_call_handler import remote_call_handler

from .federated_learning.federaed_learning_model.minst import minst_classification
from .federated_learning.federaed_learning_model.cifar10 import cifar10_classification
from .federated_learning.federaed_learning_model.synchronous_linear_regression import linear_regression
from .federated_learning.federaed_learning_model.datawarehouse import data_warehouse

import time
import random


# ------------------------ import from new version
from .fl.communications.router import router
from .fl.warehouse.warehouse import warehouse
from .fl.fl_apis.base import base


WAITING_TIME_SLOT = 0.01

class FederatedServer(BaseTask):
    def __init__(self):
        super().__init__(taskID=221, taskName='FederatedServer')
        self.potential_client_addr = []
        self.addr = None
        self.num_clients = 0
        self.machine_profile = {}

    def exec(self, inputData):

        self.addr = inputData["self_addr"]
        self.potential_client_addr.append(inputData["child_addr"])
        self.num_clients = inputData["participants"][self.taskName]["data"]["client_num"]
        self.machine_profile[inputData["child_addr"]] = inputData["machine_profile"]["cpu"], inputData["machine_profile"]["memory"]

        if len(self.potential_client_addr) < self.num_clients:
            return

        router(self.addr)
        warehouse().model_warehouse.start_ftp_server(self.addr)
        b = base()
        b.add_client(self.potential_client_addr[0])
        b.add_server(self.potential_client_addr[1])
        b.add_peer(self.potential_client_addr[2])


        while not b.get_servers() or not b.get_clients() or not b.get_peers():
            time.sleep(0.01)




        remote_server_ptr, remote_client_ptr, remote_peer_ptr = b.get_servers()[0], b.get_clients()[0], b.get_peers()[0]
        inputData = {"remote_server_ptr": [remote_server_ptr.address, remote_server_ptr.uuid], "remote_client_ptr": [remote_client_ptr.address, remote_client_ptr.uuid], "remote_peer_ptr": [remote_peer_ptr.address, remote_peer_ptr.uuid]}
        return inputData
        # set up router


    #    address, port = self.addr[0], inputData["participants"][self.taskName]["data"]["port"]
    #    addr, r = router_factory.get_router((address, port))
    #    ftp_server_factory.set_ftp_server((address, port))
    #    r.add_handler("relation__", relationship_handler())
    #    r.add_handler("communicat", model_communication_handler())
    #    r.add_handler("cli_step__", remote_call_handler())

    #    cpu_freq_factor = {}
    #    cpu_freq_sum = 0
    #    for k in self.machine_profile:
    #        cpu_freq_factor[k] = self.machine_profile[k][0]["frequency"] * (1 - self.machine_profile[k][0]["utilization"])
    #        cpu_freq_sum += cpu_freq_factor[k]


        # -------------------------------------------------------------------
    #    if inputData["participants"][self.taskName]["data"]["model"] == 'lrs':
    #        learning_rate = inputData["participants"][self.taskName]["data"]["lr"]
    #        waiting_time = inputData["participants"][self.taskName]["data"]["tim"]
    #        itr_server = inputData["participants"][self.taskName]["data"]["itr_server"]
    #        itr_client = inputData["participants"][self.taskName]["data"]["itr_client"]
    #        model = linear_regression(0.3)
    #        for client_addr in self.potential_client_addr:
    #            model.add_client(client_addr, learning_rate)

    #        while len(model.get_client()) != 3:
    #            time.sleep(0.01)

    #        for i in range(itr_server):
    #            inputData["debug_logger"].info(str(i))
    #            for ii in range(waiting_time):
    #                time.sleep(1)
    #                inputData["debug_logger"].info(str(waiting_time - ii) + " left.")

    #            for m in model.get_client():
    #                model.step_client(m, itr_client)

    #            while not model.can_federate("syn"):
    #                time.sleep(0.01)
    #            model.federate()
    #            inputData["debug_logger"].info("\nWeight: "+str(model.lr.weight))
    #            inputData["debug_logger"].info("\nBias: " + str(model.lr.bias))
    #    if inputData["participants"][self.taskName]["data"]["model"] == 'mst':
    #        selection = inputData["participants"][self.taskName]["data"]["lr"]
    #        ws = inputData["participants"][self.taskName]["data"]["ws"]
    #        itr_server = inputData["participants"][self.taskName]["data"]["itr_server"]
    #        itr_client = inputData["participants"][self.taskName]["data"]["itr_client"]

    #        model = minst_classification()
    #        if selection == 0:
    #            model.add_client(self.potential_client_addr[0], (0, 10))
    #            while len(model.get_client()) != 1:
    #                time.sleep(0.01)
    #            model.synchronous_federate_minimum_client = 1
    #        elif selection == 1:
    #            for i in range(10):
    #                model.add_client(self.potential_client_addr[i%3], (i, i + 1))
    #            while len(model.get_client()) != 10:
    #                time.sleep(0.01)
    #            model.synchronous_federate_minimum_client = 10
    #        elif selection == 2:
    #            model.add_client(self.potential_client_addr[0], (0,1))
    #            model.add_client(self.potential_client_addr[1], (1,3))
    #            model.add_client(self.potential_client_addr[2], (3,6))
    #            model.add_client(self.potential_client_addr[0], (6,10))
    #            while len(model.get_client()) != 4:
    #                time.sleep(0.01)

    #            for cli in model.get_client():
    #                model.client_performance[cli[:2]]["train_one_time"] = model.client_performance[cli[:2]]["data_size"] * 0.6

    #            model.time_allowed = 0
    #            model.synchronous_federate_minimum_client = 4
    #        elif selection == 3:
    #            model.add_client(self.potential_client_addr[0], (0,1))
    #            model.add_client(self.potential_client_addr[1], (1,3))
    #            model.add_client(self.potential_client_addr[2], (3,6))
    #            model.add_client(self.potential_client_addr[0], (6,10))
    #            while len(model.get_client()) != 4:
    #                time.sleep(0.01)
    #            ws = False
    #            model.synchronous_federate_minimum_client = 1


    #        t = time.time()
    #        for i in range(itr_server):
    #            last_accuracy = 0
    #            if selection == 2 and ws:
    #                while len(model.select_client()) == 0:
    #                    model.update_time_allowed(0.1)
    #                clients = model.select_client()
    #                model.synchronous_federate_minimum_client = len(clients)
    #                for m in clients:
    #                    model.step_client(m, itr_client)
    #            else:
    #                for m in model.get_client():
    #                    model.step_client(m, itr_client)
    #            while not model.can_federate("syn"):
    #                time.sleep(0.01)

    #            model.federate()
    #            if selection == 2 and ws:
    #                if model.should_update_time_allowed(last_accuracy, model.model.accuracy.item()):
    #                    model.update_time_allowed(0.5)
    #                last_accuracy = model.model.accuracy.item()
    #            # print(model.model.accuracy, time.time() - t)
    #            inputData["debug_logger"].info("\n\n\n\n\n")
    #            if model.model.accuracy > 80:
    #                tr1 = time.time() - t
    #                inputData["debug_logger"].info(str(model.model.accuracy.item()) + " achieved at time: " + str(tr1))
    #                break
    #            else:
    #                tr1 = time.time() - t
    #                inputData["debug_logger"].info(str(model.model.accuracy.item()) + " achieved at time: " + str(tr1))

    #            inputData["debug_logger"].info("\n\n\n\n\n")





    #    inputData = {"HI":"HIIII"}
    #    return inputData
        #for r_min in range(5):
        #    res_cifar[10][r_min] = {}
        #    res_cifar[10][r_max] = {}
        #    for r_max in range(r_min, 10):
        #        res_cifar[10][r_min][r_max] = cifar_federated_learning_r_min_rmax_cs_no_even(self.potential_client_addr, 10)
        #        res_cifar[30][r_min][r_max] = cifar_federated_learning_r_min_rmax_cs_no_even(self.potential_client_addr, 30)

        #for r_min in range(5):
        #    res_minst[10][r_min] = {}
        #    res_minst[10][r_max] = {}
        #    for r_max in range(r_min, 10):
        #        res_minst[10][r_min][r_max] = minst_federated_learning_r_min_rmax_cs_no_even(self.potential_client_addr, 10)
        #        res_minst[30][r_min][r_max] = minst_federated_learning_r_min_rmax_cs_no_even(self.potential_client_addr, 30)

        #minst_time_stamp100, minst_time_diff100, minst_accuracy100 = cifar_federated_learning_random_cs_no_even(self.potential_client_addr, 10)
        #minst_time_stamp300, minst_time_diff300, minst_accuracy300 = cifar_federated_learning_random_cs_no_even(self.potential_client_addr, 30)
        #inputData = {
        #    "minst_time_stamp100": minst_time_stamp100,
        #    "minst_time_diff100": minst_time_diff100,
        #    "minst_accuracy100": minst_accuracy100,
        #    "minst_time_stamp300": minst_time_stamp300,
        #    "minst_time_diff300": minst_time_diff300,
        #    "minst_accuracy300": minst_accuracy300
        #}

        #res = {100:{},300:{}}
        #for i in [100, 300]:
        #    for mode in ["none", "linear", "polynomial", "exponential"]:

        #        t, a = cifar_federated_learning_t_change_cs_no_even_asynchronous(self.potential_client_addr, i, cpu_freq_factor, cpu_freq_sum, mode)
        #        res[i][mode] = (t, a)
        #inputData["res"] = res

        #return inputData

def cifar_federated_learning_t_change_cs_no_even_asynchronous(client_addrs, amount, cpu_freq_factor, cpu_freq_sum, mode):
    model = cifar10_classification()
    model.synchronous_federate_minimum_client = amount
    if amount == 10:
        for i in range(3):
            model.add_client(client_addrs[0], (i*10, 30))
        for i in range(3, 6):
            model.add_client(client_addrs[1], (i*10, 60))
        for i in range(6, 10):
            model.add_client(client_addrs[2], (i*10, 100))

    if amount == 30:
        for i in range(10):
            model.add_client(client_addrs[0], (i*10, 100))
        for i in range(10, 20):
            model.add_client(client_addrs[1], (i*10, 200))
        for i in range(20, 30):
            model.add_client(client_addrs[2], (i*10, 300))

    while len(model.get_client()) < amount:
        time.sleep(0.01)

    for cli in model.get_client():
        train_one_time = cpu_freq_factor[cli[0]]/cpu_freq_sum
        model.client_performance[cli[:2]]["train_one_time"] = train_one_time

    time_stamp = [time.time()]
    time_diff = [0]
    accuracy = [model.model.accuracy]
    model.time_allowed = 0
    while len(model.select_client()) == 0:
        model.update_time_allowed(0.1)


    for i in range(100):
        while len(model.select_client()) == 0:
            model.update_time_allowed(0.1)
        clients = model.select_client()
        model.synchronous_federate_minimum_client = len(clients)

        for cli in clients:
            model.step_client(cli, 10)

        while not model.can_federate("asyn"):
            time.sleep(0.01)

        model.federate(federation_algo=mode)

        accuracy.append(model.model.accuracy.item())
        time_stamp.append(time.time())
        time_diff.append(time_stamp[-1] - time_stamp[-2])

        if model.should_update_time_allowed(accuracy[-1], accuracy[-2]):
            model.update_time_allowed(0.2)
        if model.should_early_terminate(accuracy, 0.2):
            print("Early Terminate")
            break
    return time_diff, accuracy

def minst_federated_learning_t_change_cs_no_even_asynchronous(client_addrs, amount, cpu_freq_factor, cpu_freq_sum, mode):
    model = minst_classification()
    model.synchronous_federate_minimum_client = amount
    if amount == 10:
        for i in range(3):
            model.add_client(client_addrs[0], (i, 3))
        for i in range(3, 6):
            model.add_client(client_addrs[1], (i, 6))
        for i in range(6, 10):
            model.add_client(client_addrs[2], (i, 10))

    if amount == 30:
        for i in range(10):
            model.add_client(client_addrs[0], (i, 10))
        for i in range(10, 20):
            model.add_client(client_addrs[1], (i, 20))
        for i in range(20, 30):
            model.add_client(client_addrs[2], (i, 30))

    while len(model.get_client()) < amount:
        time.sleep(0.01)

    for cli in model.get_client():
        train_one_time = cpu_freq_factor[cli[0]] / cpu_freq_sum
        model.client_performance[cli[:2]]["train_one_time"] = train_one_time

    time_stamp = [time.time()]
    time_diff = [0]
    accuracy = [model.model.accuracy]
    model.time_allowed = 0
    while len(model.select_client()) == 0:
        model.update_time_allowed(0.1)

    for i in range(100):
        while len(model.select_client()) == 0:
            model.update_time_allowed(0.1)
        clients = model.select_client()
        model.synchronous_federate_minimum_client = len(clients)

        for cli in clients:
            model.step_client(cli, 10)

        while not model.can_federate("asyn"):
            time.sleep(0.01)

        model.federate(federation_algo=mode)

        accuracy.append(model.model.accuracy.item())
        time_stamp.append(time.time())
        time_diff.append(time_stamp[-1] - time_stamp[-2])

        if model.should_update_time_allowed(accuracy[-1], accuracy[-2]):
            model.update_time_allowed(0.5)
        if model.should_early_terminate(accuracy, 1):
            print("Early Terminate")
            break
    return time_diff, accuracy

def cifar_federated_learning_t_change_cs_no_even(client_addrs, amount, cpu_freq_factor, cpu_freq_sum, mode):
    model = cifar10_classification()
    model.synchronous_federate_minimum_client = amount
    if amount == 10:
        for i in range(3):
            model.add_client(client_addrs[0], (i*10, 30))
        for i in range(3, 6):
            model.add_client(client_addrs[1], (i*10, 60))
        for i in range(6, 10):
            model.add_client(client_addrs[2], (i*10, 100))

    if amount == 30:
        for i in range(10):
            model.add_client(client_addrs[0], (i*10, 100))
        for i in range(10, 20):
            model.add_client(client_addrs[1], (i*10, 200))
        for i in range(20, 30):
            model.add_client(client_addrs[2], (i*10, 300))

    while len(model.get_client()) < amount:
        time.sleep(0.01)

    for cli in model.get_client():
        train_one_time = cpu_freq_factor[cli[0]]/cpu_freq_sum
        model.client_performance[cli[:2]]["train_one_time"] = train_one_time

    time_stamp = [time.time()]
    time_diff = [0]
    accuracy = [model.model.accuracy]
    model.time_allowed = 0
    while len(model.select_client()) == 0:
        model.update_time_allowed(0.1)


    for i in range(100):
        while len(model.select_client()) == 0:
            model.update_time_allowed(0.1)
        clients = model.select_client()
        model.synchronous_federate_minimum_client = len(clients)

        for cli in clients:
            model.step_client(cli, 10)

        while not model.can_federate():
            time.sleep(0.01)

        model.federate(federation_algo=mode)

        accuracy.append(model.model.accuracy.item())
        time_stamp.append(time.time())
        time_diff.append(time_stamp[-1] - time_stamp[-2])

        if model.should_update_time_allowed(accuracy[-1], accuracy[-2]):
            model.update_time_allowed(0.2)
        if model.should_early_terminate(accuracy, 0.2):
            print("Early Terminate")
            break
    return time_diff, accuracy
def minst_federated_learning_t_change_cs_no_even(client_addrs, amount, cpu_freq_factor, cpu_freq_sum, mode):
    model = minst_classification()
    model.synchronous_federate_minimum_client = amount
    if amount == 10:
        for i in range(3):
            model.add_client(client_addrs[0], (i, 3))
        for i in range(3, 6):
            model.add_client(client_addrs[1], (i, 6))
        for i in range(6, 10):
            model.add_client(client_addrs[2], (i, 10))

    if amount == 30:
        for i in range(10):
            model.add_client(client_addrs[0], (i, 10))
        for i in range(10, 20):
            model.add_client(client_addrs[1], (i, 20))
        for i in range(20, 30):
            model.add_client(client_addrs[2], (i, 30))

    while len(model.get_client()) < amount:
        time.sleep(0.01)

    for cli in model.get_client():
        train_one_time = cpu_freq_factor[cli[0]]/cpu_freq_sum
        model.client_performance[cli[:2]]["train_one_time"] = train_one_time

    time_stamp = [time.time()]
    time_diff = [0]
    accuracy = [model.model.accuracy]
    model.time_allowed = 0
    while len(model.select_client()) == 0:
        model.update_time_allowed(0.1)


    for i in range(100):
        while len(model.select_client()) == 0:
            model.update_time_allowed(0.1)
        clients = model.select_client()
        model.synchronous_federate_minimum_client = len(clients)

        for cli in clients:
            model.step_client(cli, 10)

        while not model.can_federate():
            time.sleep(0.01)

        model.federate(federation_algo=mode)

        accuracy.append(model.model.accuracy.item())
        time_stamp.append(time.time())
        time_diff.append(time_stamp[-1] - time_stamp[-2])

        if model.should_update_time_allowed(accuracy[-1], accuracy[-2]):
            model.update_time_allowed(0.5)
        if model.should_early_terminate(accuracy, 1):
            print("Early Terminate")
            break
    return time_diff, accuracy

def minst_federated_learning_r_min_rmax_cs_no_even(client_addrs, amount):
    model = minst_classification()
    model.r_min = 5
    model.r_max = 5
    if amount == 10:
        for i in range(3):
            model.add_client(client_addrs[0], (i, 3))
        for i in range(3, 6):
            model.add_client(client_addrs[1], (i, 6))
        for i in range(6, 10):
            model.add_client(client_addrs[2], (i, 10))

    if amount == 30:
        for i in range(10):
            model.add_client(client_addrs[0], (i, 10))
        for i in range(10, 20):
            model.add_client(client_addrs[1], (i, 20))
        for i in range(20, 30):
            model.add_client(client_addrs[2], (i, 30))

    while len(model.get_client()) < amount:
        time.sleep(WAITING_TIME_SLOT)

    time_stamp = [time.time()]
    time_diff = [0]
    accuracy = [model.model.accuracy]

    for i in range(100):
        top_k = model.select_top_k()
        model.synchronous_federate_minimum_client = len(top_k)
        for cli in top_k:
            model.step_client(cli, 10)
        while not model.can_federate():
            time.sleep(0.01)

        accuracy_old = model.model.accuracy
        if accuracy_old != 0: accuracy_old = accuracy_old.item()
        model.federate()
        accuracy_new = model.model.accuracy.item()
        model.update_r(accuracy_new, accuracy_old)

        time_stamp.append(time.time())
        time_diff.append(time_stamp[-1] - time_stamp[-2])
        accuracy.append(model.model.accuracy.item())

    return time_stamp, time_diff, accuracy

def cifar_federated_learning_r_min_rmax_cs_no_even(client_addrs, amount):
    model = cifar10_classification()
    if amount == 10:
        for i in range(3):
            model.add_client(client_addrs[0], (i*10, 30))
        for i in range(3, 6):
            model.add_client(client_addrs[1], (i*10, 60))
        for i in range(6, 10):
            model.add_client(client_addrs[2], (i*10, 100))

    if amount == 30:
        for i in range(10):
            model.add_client(client_addrs[0], (i*10, 100))
        for i in range(10, 20):
            model.add_client(client_addrs[1], (i*10, 200))
        for i in range(20, 30):
            model.add_client(client_addrs[2], (i*10, 300))

    while len(model.get_client()) < amount:
        time.sleep(WAITING_TIME_SLOT)

    time_stamp = [time.time()]
    time_diff = [0]
    accuracy = [model.model.accuracy]

    for i in range(100):
        top_k = model.select_top_k()
        model.synchronous_federate_minimum_client = len(top_k)
        for cli in top_k:
            model.step_client(cli, 10)
        while not model.can_federate():
            time.sleep(0.01)

        accuracy_old = model.model.accuracy
        if accuracy_old != 0: accuracy_old = accuracy_old.item()
        model.federate()
        accuracy_new = model.model.accuracy.item()
        model.update_r(accuracy_new, accuracy_old)

        time_stamp.append(time.time())
        time_diff.append(time_stamp[-1] - time_stamp[-2])
        accuracy.append(model.model.accuracy.item())

    return time_stamp, time_diff, accuracy


def minst_federated_learning_random_cs_no_even(client_addrs, amount):
    model = minst_classification()
    model.synchronous_federate_minimum_client = 3
    if amount == 10:
        for i in range(3):
            model.add_client(client_addrs[0], (i, 3))
        for i in range(3, 6):
            model.add_client(client_addrs[1], (i, 6))
        for i in range(6, 10):
            model.add_client(client_addrs[2], (i, 10))

    if amount == 30:
        for i in range(10):
            model.add_client(client_addrs[0], (i, 10))
        for i in range(10, 20):
            model.add_client(client_addrs[1], (i, 20))
        for i in range(20, 30):
            model.add_client(client_addrs[2], (i, 30))

    while len(model.get_client()) < amount:
        time.sleep(WAITING_TIME_SLOT)

    time_stamp = [time.time()]
    time_diff = [0]
    accuracy = [model.model.accuracy]
    for i in range(100):
        for cli in random.sample(model.get_client(), 3):
            model.step_client(cli, 10)
        while not model.can_federate():
            time.sleep(0.01)
        model.federate()
        time_stamp.append(time.time())
        time_diff.append(time_stamp[-1] - time_stamp[-2])
        accuracy.append(model.model.accuracy.item())

    return time_stamp, time_diff, accuracy

def cifar_federated_learning_random_cs_no_even(client_addrs, amount):
    model = cifar10_classification()
    model.synchronous_federate_minimum_client = 3
    if amount == 10:
        for i in range(3):
            model.add_client(client_addrs[0], (i, 30))
        for i in range(3, 6):
            model.add_client(client_addrs[1], (i, 60))
        for i in range(6, 10):
            model.add_client(client_addrs[2], (i, 100))

    if amount == 30:
        for i in range(10):
            model.add_client(client_addrs[0], (i, 100))
        for i in range(10, 20):
            model.add_client(client_addrs[1], (i, 200))
        for i in range(20, 30):
            model.add_client(client_addrs[2], (i, 300))

    while len(model.get_client()) < amount:
        time.sleep(WAITING_TIME_SLOT)

    time_stamp = [time.time()]
    time_diff = [0]
    accuracy = [model.model.accuracy]
    for i in range(100):
        for cli in random.sample(model.get_client(), 3):
            model.step_client(cli, 5)
        while not model.can_federate():
            time.sleep(0.01)
        model.federate()
        time_stamp.append(time.time())
        time_diff.append(time_stamp[-1] - time_stamp[-2])
        accuracy.append(model.model.accuracy.item())

    return time_stamp, time_diff, accuracy

def minst_federated_learning_no_cs_no_even(client_addrs, amount):
    model = minst_classification()
    model.synchronous_federate_minimum_client = amount
    if amount == 10:
        for i in range(3):
            model.add_client(client_addrs[0], (i,3))
        for i in range(3,6):
            model.add_client(client_addrs[1], (i,6))
        for i in range(6,10):
            model.add_client(client_addrs[2], (i,10))

    if amount == 30:
        for i in range(10):
            model.add_client(client_addrs[0], (i,10))
        for i in range(10,20):
            model.add_client(client_addrs[1], (i,20))
        for i in range(20,30):
            model.add_client(client_addrs[2], (i,30))

    while len(model.get_client()) < amount:
        time.sleep(WAITING_TIME_SLOT)

    time_stamp = [time.time()]
    time_diff = [0]
    accuracy = [model.model.accuracy]
    for i in range(100):
        for cli in model.get_client():
            model.step_client(cli, 10)
        while not model.can_federate():
            time.sleep(0.01)
        model.federate()
        time_stamp.append(time.time())
        time_diff.append(time_stamp[-1]-time_stamp[-2])
        accuracy.append(model.model.accuracy.item())

    return time_stamp, time_diff, accuracy

def cifar_federated_learning_no_cs_no_even(client_addrs, amount):
    model = cifar10_classification()
    model.synchronous_federate_minimum_client = amount
    if amount == 10:
        for i in range(3):
            model.add_client(client_addrs[0], (i*10,30))
        for i in range(3,6):
            model.add_client(client_addrs[1], (i*10,60))
        for i in range(6,10):
            model.add_client(client_addrs[2], (i*10,100))

    if amount == 30:
        for i in range(10):
            model.add_client(client_addrs[0], (i*10,100))
        for i in range(10,20):
            model.add_client(client_addrs[1], (i*10,200))
        for i in range(20,30):
            model.add_client(client_addrs[2], (i*10,300))

    while len(model.get_client()) < amount:
        time.sleep(WAITING_TIME_SLOT)

    time_stamp = [time.time()]
    time_diff = [0]
    accuracy = [model.model.accuracy]
    for i in range(50):
        for cli in model.get_client():
            model.step_client(cli, 5)
        while not model.can_federate():
            time.sleep(0.01)
        model.federate()
        time_stamp.append(time.time())
        time_diff.append(time_stamp[-1]-time_stamp[-2])
        accuracy.append(model.model.accuracy.item())

    return time_stamp, time_diff, accuracy

def minst_federated_learning_no_cs_even(client_addrs, amount):
    model = minst_classification()
    model.synchronous_federate_minimum_client = amount
    if amount == 10:
        for i in range(3):
            model.add_client(client_addrs[0], (i,i+1))
        for i in range(3,6):
            model.add_client(client_addrs[1], (i,i+1))
        for i in range(6,10):
            model.add_client(client_addrs[2], (i,i+1))

    if amount == 30:
        for i in range(10):
            model.add_client(client_addrs[0], (i,i+1))
        for i in range(10,20):
            model.add_client(client_addrs[1], (i,i+1))
        for i in range(20,30):
            model.add_client(client_addrs[2], (i,i+1))

    while len(model.get_client()) < amount:
        time.sleep(WAITING_TIME_SLOT)

    time_stamp = [time.time()]
    time_diff = [0]
    accuracy = [model.model.accuracy]
    for i in range(100):
        for cli in model.get_client():
            model.step_client(cli, 10)
        while not model.can_federate():
            time.sleep(0.01)
        model.federate()
        time_stamp.append(time.time())
        time_diff.append(time_stamp[-1]-time_stamp[-2])
        accuracy.append(model.model.accuracy.item())

    return time_stamp, time_diff, accuracy

def cifar_federated_learning_no_cs_even(client_addrs, amount):
    model = cifar10_classification()
    model.synchronous_federate_minimum_client = amount
    if amount == 10:
        for i in range(3):
            model.add_client(client_addrs[0], (i*10,(i+1)*10))
        for i in range(3,6):
            model.add_client(client_addrs[1], (i*10,(i+1)*10))
        for i in range(6,10):
            model.add_client(client_addrs[2], (i*10,(i+1)*10))

    if amount == 30:
        for i in range(10):
            model.add_client(client_addrs[0], (i*10,(i+1)*10))
        for i in range(10,20):
            model.add_client(client_addrs[1], (i*10,(i+1)*10))
        for i in range(20,30):
            model.add_client(client_addrs[2], (i*10,(i+1)*10))

    while len(model.get_client()) < amount:
        time.sleep(WAITING_TIME_SLOT)

    time_stamp = [time.time()]
    time_diff = [0]
    accuracy = [model.model.accuracy]
    for i in range(50):
        for cli in model.get_client():
            model.step_client(cli, 5)
        while not model.can_federate():
            time.sleep(0.01)
        model.federate()
        time_stamp.append(time.time())
        time_diff.append(time_stamp[-1]-time_stamp[-2])
        accuracy.append(model.model.accuracy.item())

    return time_stamp, time_diff, accuracy

def minst_sequential_test(client_addr, amount):
    model = minst_classification()
    model.synchronous_federate_minimum_client = 1
    model.add_client(client_addr, (0,amount))
    while len(model.get_client()) == 0:
        time.sleep(WAITING_TIME_SLOT)

    time_stamp = [time.time()]
    time_diff = [0]
    accuracy = [model.model.accuracy]

    for i in range(100):
        model.step_client(model.get_client()[0], 1)
        while not model.can_federate():
            time.sleep(0.01)
        model.federate()
        time_stamp.append(time.time())
        time_diff.append(time_stamp[-1]-time_stamp[-2])
        accuracy.append(model.model.accuracy.item())

    return time_stamp, time_diff, accuracy

def cifar_sequential_test(client_addr, amount):
    model = cifar10_classification()
    model.synchronous_federate_minimum_client = 1
    model.add_client(client_addr, (0, amount))
    while len(model.get_client()) == 0:
        time.sleep(WAITING_TIME_SLOT)

    time_stamp = [time.time()]
    time_diff = [0]
    accuracy = [model.model.accuracy]

    for i in range(100):
        model.step_client(model.get_client()[0], 5)
        while not model.can_federate():
            time.sleep(0.01)
        model.federate()
        time_stamp.append(time.time())
        time_diff.append(time_stamp[-1]-time_stamp[-2])
        accuracy.append(model.model.accuracy.item())

    return time_stamp, time_diff, accuracy

