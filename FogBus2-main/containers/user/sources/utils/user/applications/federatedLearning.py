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

        inputData = {
            "number": 1,
            "tag": "Federated Learning"
        }

        # put it in to data uploading queue
        self.dataToSubmit.put(inputData)

        # wait for all the 4 results

        while True:
            result = self.resultForActuator.get()
            self.basicComponent.debugLogger.info('Done: the result is: %s', result)
            self.basicComponent.debugLogger.info('--------------------------XXX-------------------------')
