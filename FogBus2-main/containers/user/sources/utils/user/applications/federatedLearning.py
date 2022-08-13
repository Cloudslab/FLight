from time import time
from pprint import pformat

from numpy.core.defchararray import isnumeric

from .base import ApplicationUserSide
from ...component.basic import BasicComponent


class FederatedLearning(ApplicationUserSide):

    def __init__(
            self,
            videoPath: str,
            targetHeight: int,
            showWindow: bool,
            basicComponent: BasicComponent):
        super().__init__(
            appName='FederatedLearning',
            videoPath=videoPath,
            targetHeight=targetHeight,
            showWindow=showWindow,
            basicComponent=basicComponent)
        self.count = 3

    def prepare(self):
        pass

    def _run(self):
        self.basicComponent.debugLogger.info(
            'Application is running: %s', self.appName)

        print("FogBus2 -- Federated Learning")
        print("Set Up:")
        print("---------------------------------------------------")
        print("3 Workers, 1 Server, 0 Peer Connection")
        print("---------------------------------------------------")
        print("Workers: federatedWorker0, federatedWorker1, federatedWorker2")
        print("---------------------------------------------------")
        print("Server: federatedServer")
        print("---------------------------------------------------")
        print("federatedWorker0 --> federatedServer")
        print("federatedWorker1 --> federatedServer")
        print("federatedWorker1 --> federatedServer")
        print("---------------------------------------------------")

        # aggregate iteration
        print("Aggregate Iteration on federatedServer, (itr_server > 0): ", end="")
        itr_server = int(input())
        assert (itr_server > 0)
        print("Aggregate Iteration on federatedWorkers, (itr_client > 0): ", end="")
        itr_client = int(input())
        assert (itr_client > 0)

        # time between each aggregation
        print("Waiting time between each federated training, (tim >= 0)", end="")
        tim = int(input())
        assert (tim >= 0)

        # linear regression
        print("Select Model \n [0] linear regression \n Your Selection: ", end="")
        model = None
        if input() == "0":
            model = 'lr'
        else:
            return

        # parameter for lr
        print("Linear Regression: Y = Wx + B")
        print("Initial W value: ", end="")
        w = float(input())
        print("Initial B value:")
        b = float(input())
        print("Initial learning rate:", end="")
        lr = float(input())


        federatedWorker0 = {
            "role": "client",
            "data": {
                "port":54321
            }
        }

        federatedWorker1 = {
            "role": "client",
            "data": {
                "port":54322
            }
        }

        federatedWorker2 = {
            "role": "client",
            "data": {
                "port":54323
            }
        }

        federatedServer = {
            "role": "server",
            "data": {
                "client_num": 3,
                "port": 54324,
                "tim": tim,
                "itr_client": itr_client,
                "itr_server": itr_server,
                "lr": lr,
                "b": b,
                "w": w,
                "model": model
            }
        }


        inputData = {
            "participants":{
                "FederatedLearning0": federatedWorker0,
                "FederatedLearning1": federatedWorker1,
                "FederatedLearning2": federatedWorker2,
                "FederatedServer": federatedServer
            },
            "tag": "Federated Learning"
        }

        # put it in to data uploading queue
        self.dataToSubmit.put(inputData)

        # wait for all the 4 results

        while True:
            result = self.resultForActuator.get()
            self.basicComponent.debugLogger.info('Done: the result is: %s', result)
            self.basicComponent.debugLogger.info('--------------------------XXX-------------------------')
        return
