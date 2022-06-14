import time

from core.ml.model.LinearRegression import LinearRegressionFactory
from core.fl.horizontal.FedAvg import fed_avg
from core.communication.routing.router import Router

if __name__ == "__main__":


    model = LinearRegressionFactory().LinearRegressionServer(1,1,0.01,["10.211.55.4",5000])

    model.request_worker(["10.211.55.13",5000])
    model.request_worker(["10.211.55.16", 5000])
    while len(model.worker_ptrs) < 2:
        time.sleep(1)

    epoch = 300
    i = 0
    while i < epoch:
        model.notify_all()
        while model.waiting_next_round < 2:
            pass

        model.push_all_client_train()
        while len(model.w_list) < 2:
            pass

        model.fl_step(fed_avg)
        model.next()
        i+=1
    print(model.export())

    #while len(model.worker_ptrs) < 4:
    #    pass
    #
    #model.notify_all()
    #
    #while model.waiting_next_round < 4:
    #    print("aaa")
    #
    #model.push_all_client_train()
    #
    #while len(model.w_list) < 4:
    #    print("bbb")
    #
    #model.fl_step(fed_avg)
    #model.next()
    #print(model.export())
    #print(model.__dict__)