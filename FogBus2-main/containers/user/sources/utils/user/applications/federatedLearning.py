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

        inputData = {
            "default_data_param": {
                "w1l":w1l,
                "w1s":w1s,
                "w2l":w2l,
                "w2s":w2s,
                "w3l":w3l,
                "w3s":w3s
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
