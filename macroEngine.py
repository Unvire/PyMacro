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

    def __str__(self):
        nameString = f'Task:{self.name}| state:{self.isEnabled}| '
        functionString = f'function:{self.executeFunction.__name__}, package:{self.executeFunction.__globals__["__name__"]}| '
        parametersString = f'parameters:{self.parameters}'
        return nameString + functionString + parametersString

class MacroEngine:
    def __init__(self):
        self.taskList = []
        self.numOfTasks = 0

    def numOfTasksGetSet(self):
        '''
        Getter and setter of self.numOfTasks
        '''
        self.numOfTasks = len(self.taskList)
        return self.numOfTasks

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
        Opens json file, converts data from dictionary to Task instances and appends them to self.taskList.
            filePath - path to JSON file
        '''
        with open(filePath, 'r') as file:
            taskDict = json.load(file)

        for taskID in taskDict:
            task = self._createTask(taskDict=taskDict[taskID])
            self.taskList.append(task)

    def saveJSON(self):
        pass

    def executeTask(self, task):
        '''
        Executes task by calling function in task.executeFunction with keyword arguments given in task.parameters. Returns time of execution
            task: instance of Task class
        '''
        timerStart = timer()
        if task.isEnabled:
            task.executeFunction(**task.parameters)
        timerEnd = timer()
        return timerEnd - timerStart
    
    def runProgram(self):
        '''
        Runs macro by iterating over self.taskList and executing task
        '''
        for task in self.taskList:
            elapsedTime = self.executeTask(task)
            print(elapsedTime)


if __name__ == '__main__':
    engine = MacroEngine()
    engine.loadJSON('macro.json')
    engine.runProgram()