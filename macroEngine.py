import json
from timeit import default_timer as timer

import keyboardFunctions, cursorFunctions, imageFunctions, logicFunctions, clipboardFunctions

class Task:
    def __init__(self, name='', isEnabled=False, executeFunction=None, parameters=None, isJump=False, variableName=None):
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
        self.isJump = isJump
        self.variableName = variableName

    def __str__(self):
        nameString = f'Task:{self.name}| state:{self.isEnabled}| '
        functionString = f'function:{self.executeFunction.__name__}, package:{self.executeFunction.__globals__["__name__"]}| '
        parametersString = f'parameters:{self.parameters}, isJump:{self.isJump}, variableName:{self.variableName}'
        return nameString + functionString + parametersString

    def convertToDict(self):
        '''
        Returns dictionary representation
        '''
        functionString = f'{self.executeFunction.__globals__["__name__"]}.{self.executeFunction.__name__}'
        return {'name':self.name, 'enabled':self.isEnabled, 'function':functionString, 'isJump':self.isJump, 
                'parameters':self.parameters, 'saveResultToVariable':{self.variableName}}

class MacroEngine():
    def __init__(self, variablesDict={}):
        self.taskList = []
        self.numOfTasks = 0
        self.variables = variablesDict

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
        isJump = taskDict['isJump']
        parameters = taskDict['parameters']
        variableName = taskDict['saveResultToVariable']

        taskInstance = Task(name=name, isEnabled=isEnabled, executeFunction=taskFunction, parameters=parameters, isJump=isJump, variableName=variableName)
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
            self.numOfTasksGetSet()

    def saveJSON(self, filePath):
        '''
        Saves self.taskList to file.
            filePath - path where program will save JSON. Must inlcude file name
        '''
        taskDict = {}
        for i, task in enumerate(self.taskList):
            taskDict[str(i)] = task.convertToDict()
        
        with open(filePath, 'w') as file:
            json.dump(taskDict, file, indent=2)

    def executeTask(self, task):
        '''
        Executes task by calling function in task.executeFunction with keyword arguments given in task.parameters. Returns time of execution and result of task
            task: instance of Task class
        '''
        timerStart = timer()
        if task.isEnabled:
            result = task.executeFunction(**task.parameters)
            if task.variableName:
                self.variables[task.variableName] = result
        timerEnd = timer()
        return timerEnd - timerStart, result
    
    def runProgram(self):
        '''
        Runs macro by iterating over self.taskList and executing task
        '''
        self.numOfTasksGetSet()
        currentTaskID = 0
        
        ## while loop allows to change currentTaskID programatically (loop back and forward)
        while currentTaskID < self.numOfTasks:
            task = self.taskList[currentTaskID]
            elapsedTime, result = self.executeTask(task)
            
            print(elapsedTime)
            if result and task.isJump:
                currentTaskID = int(result)
            else:
                currentTaskID += 1


if __name__ == '__main__':
    variables = {}
    engine = MacroEngine(variablesDict = variables)
    engine.loadJSON('macro.json')
    engine.runProgram()
    #engine.saveJSON('saveTest.json')
    print(variables)