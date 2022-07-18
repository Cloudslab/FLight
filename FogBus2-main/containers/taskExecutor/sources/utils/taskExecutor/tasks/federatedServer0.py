from .base import BaseTask


class FederatedServer0(BaseTask):
    def __init__(self):
        super().__init__(taskID=203, taskName='FederatedServer0')
        self.id0 = None
        self.id1 = None
        self.id2 = None
    def exec(self, inputData):

        if 'taskID0' in inputData:
            self.id0 = inputData['taskID0']
        if 'taskID1' in inputData:
            self.id1 = inputData['taskID1']
        if 'taskID0' in inputData:
            self.id2 = inputData['taskID2']

        if self.id0 is None:
            return
        if self.id1 is None:
            return
        if self.id2 is None:
            return

        inputData['taskID0'] = self.id0
        inputData['taskID1'] = self.id1
        inputData['taskID2'] = self.id2
        inputData['serverID'] = self.taskID
        return inputData