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

    def prepare(self):
        pass

    def _run(self):
        self.basicComponent.debugLogger.info(
            'Application is running: %s', self.appName)

        inputData = {
        }

        # put it in to data uploading queue
        self.dataToSubmit.put(inputData)
        lastDataSentTime = time()

        # wait for all the 4 results
        while True:
            result = self.resultForActuator.get()

            responseTime = (time() - lastDataSentTime) * 1000
            self.responseTime.update(responseTime)
            self.responseTimeCount += 1

            self.basicComponent.debugLogger.info("still waiting--------------------------")

            if 'taskID0' in result and 'taskID1' in result and 'taskID2' in result:
                break

        self.basicComponent.debugLogger.info(
            'Received all the 3 ID: \r\n%s', pformat(result))
