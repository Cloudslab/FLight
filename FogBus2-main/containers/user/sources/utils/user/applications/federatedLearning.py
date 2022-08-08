from time import time
from pprint import pformat
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

        print('worker_1_data_length = ', end='')
        w1l = int(input())
        print('worker_1_data_scalar = ', end='')
        w1s = int(input())
        print('worker_2_data_length = ', end='')
        w2l = int(input())
        print('worker_2_data_scalar = ', end='')
        w2s = int(input())
        print('worker_3_data_length = ', end='')
        w3l = int(input())
        print('worker_3_data_scalar = ', end='')
        w3s = int(input())

        federatedWorker0 = {
            "role": "client",
            "data": {
                "default_data_len":w1l,
                "default_data_scalar":w1s,
                "port":54321
            }
        }

        federatedWorker1 = {
            "role": "client",
            "data": {
                "default_data_len": w2l,
                "default_data_scalar": w2s,
                "port":54322
            }
        }

        federatedWorker2 = {
            "role": "client",
            "data": {
                "default_data_len": w3l,
                "default_data_scalar": w3s,
                "port":54323
            }
        }

        federatedServer = {
            "role": "server",
            "data": {
                "client_num": 3,
                "port": 54324
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
