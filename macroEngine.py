import json
from timeit import default_timer as timer

import keyboardFunctions
import cursorFunctions
import imageFunctions

class Task:
    def __init__(self, name='', isEnabled=False, executeFunction=None, parameters=None):
        '''
        name: str -> name of the task
        isEnabled: bool -> disabled task are not executed
        executeFunction -> reference for function to be executed
        parameters: dict -> dictionary of parameters, that are passed as keyword arguments to executeFunction 
        '''
        self.name = name
        self.isEnabled = isEnabled
        self.executeFunction = executeFunction
        self.parameters =  parameters

class MacroEngine:
    def __init__(self):
        self.taskList = []

    def _createTask(self, taskDict=None):
        '''
        Converts taskDict to instance of Task class. Reuturns that instance
        '''
        name = taskDict['name']
        isEnabled = taskDict['enabled']
        packageName, taskName = taskDict['function'].split('.')  
        taskPackage = globals()[packageName]
        taskFunction = getattr(taskPackage, taskName)
        parameters = taskDict['parameters']

        taskInstance = Task(name=name, isEnabled=isEnabled, executeFunction=taskFunction, parameters=parameters)
        return taskInstance
        

    def loadJSON(self, filePath):
        '''
        Opens json file, converts data from dictionary to Task instances and appends them to self.taskList
        '''
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