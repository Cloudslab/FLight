from core.ml.model.LinearRegression import LinearRegressionFactory
from core.fl.horizontal.FedAvg import fed_avg

if __name__ == "__main__":
    #model = LinearRegressionFactory().LinearRegressionServer(1,1,0.01,["127.0.0.1",5000])
    #
    #model.request_worker(["127.0.0.1",5000])
    #model.request_worker(["127.0.0.1", 5000])
    #model.request_worker(["127.0.0.1", 5000])
    #model.request_worker(["127.0.0.1", 5000])
    #
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
    print("Import success")