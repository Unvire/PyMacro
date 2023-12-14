import json
from timeit import default_timer as timer

import keyboardFunctions
import cursorFunctions
import imageFunctions

class Task:
    pass

class MacroEngine:
    def __init__(self):
        self.taskList = []

    def _createTask(self, taskDict=None):
        name = taskDict['name']
        isEnabled = taskDict['enabled']
        packageName, taskName = taskDict['function'].split('.')  
        taskPackage = globals()[packageName]
        taskFunction = getattr(taskPackage, taskName)
        parameters = taskDict['parameters']

        taskInstance = Task()
        return taskInstance
        

    def loadJSON(self, filePath):
        with open(filePath, 'r') as file:
            taskDict = json.load(file)

        for taskID in taskDict:
            self._createTask(taskDict=taskDict[taskID])

    def saveJSON(self):
        pass

    def executeTask(self):
        pass

if __name__ == '__main__':
    engine = MacroEngine()
    engine.loadJSON('macro.json')