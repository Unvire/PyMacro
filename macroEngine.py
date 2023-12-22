import os
import json
from timeit import default_timer as timer
import importlib
import task

class MacroEngine():
    def __init__(self):
        '''
        self.taskList: list[tasks] -> list of tasks to be executed in order from 0 to last item
        self.numOfTasks: int -> length of self.taskList
        self.variables: dict -> variables dictionary for program and user
        self.modules: dict -> dictionary with dynamically imported modules when creating tasks
        self.subscribers: list => list with objects that observe this engine
        '''
        self.taskList = []
        self.numOfTasks = 0
        self.variables = {}
        self.modules = {}
        self.subscribers = [] 

    def _createTask(self, taskDict=None):
        '''
        Converts taskDict to instance of Task class. Returns instance of Task class
        '''
        name = taskDict['name']
        isEnabled = taskDict['enabled']
        parameters = taskDict['parameters']        
        variableName = taskDict['saveResultToVariable']

        ## get module and function by their string name
        packageName, taskName = taskDict['function'].split('.')  
        packageName = '.' + packageName

        ## import package from functions folder
        if packageName not in self.modules:
            self.modules[packageName] = importlib.import_module(packageName, package='functions')
        
        ## get requested function from that package
        taskFunction = getattr(self.modules[packageName], taskName)

        ## check if task is a conditional jump
        if taskName == 'checkCondition' and 'isJump' in parameters:
            isJump = parameters['isJump']
            parameters.pop('isJump')
        else:            
            isJump = False

        ## load parameters from self.variables dict. (key:(parameterValue, parameterName))
        for parameter in parameters:
            parameterValue = parameters[parameter]
            parameterName = None
            if isinstance(parameterValue, str) and parameterValue in self.variables:
                parameterName = parameterValue
                parameterValue = self.variables[parameterValue]
            parameters[parameter] = parameterValue, parameterName

        taskInstance = task.Task(name=name, isEnabled=isEnabled, executeFunction=taskFunction, parameters=parameters, isJump=isJump, variableName=variableName)
        return taskInstance
    
    def numOfTasksGetSet(self):
        '''
        Getter and setter of self.numOfTasks
        '''
        self.numOfTasks = len(self.taskList)
        return self.numOfTasks

    def registerSubscriber(self, subscriber):
        '''
        Add subscriber(object) to the list. Object must implement 'update' interface
        '''
        self.subscribers.append(subscriber)
    
    def notify(self, taskID=None, elapsedTime=None):
        '''
        Broadcast status to all subscribers
        '''
        for subscriber in self.subscribers:
            subscriber.update(taskID=taskID, elapsedTime=elapsedTime)
    

    def loadMacroFile(self, filePath):
        '''
        Opens json file, converts data from dictionary to Task instances and appends them to self.taskList.
            filePath - path to JSON file
        '''
        with open(filePath, 'r') as file:
            taskDict = json.load(file)

        ## convert json to task list
        for taskID in taskDict:
            task = self._createTask(taskDict=taskDict[taskID])
            self.taskList.append(task)
            self.numOfTasksGetSet()

    def saveMacroToFile(self, filePath):
        '''
        Saves self.taskList to file.
            filePath - path where program will save JSON. Must inlcude file name
        '''
        taskDict = {}
        for i, task in enumerate(self.taskList):
            taskDict[str(i)] = task.convertToDict()
        
        with open(filePath, 'w') as file:
            json.dump(taskDict, file, indent=2)
    
    def loadVariablesFile(self, filePath):
        '''
        Loads variables from JSON file
        '''
        with open(filePath, 'r') as file:
            self.variables = json.load(file)
    
    def saveVariablesToFile(self, filePath):
        '''
        Loads variables from JSON file
        '''
        with open(filePath, 'w') as file:
            json.dump(self.variables, file, indent=2)
    
    def loadVariablesMacro(self, dirPath:str, fileName:str):
        '''
        Loads variables from json and then macro. Both of the files must be in the same directory.
            dirPath -> path to macro directory
            fileName -> name of the macro program
        '''
        variablesPath = os.path.join(dirPath, 'variables.json')
        self.loadVariablesFile(variablesPath)
        macroPath = os.path.join(dirPath, fileName)
        self.loadMacroFile(macroPath)

    def executeTask(self, task, taskID):
        '''
        Executes task by calling function in task.executeFunction with keyword arguments given in task.parameters. Returns time of execution and result of task
            task: instance of Task class
        '''
        timerStart = timer()
        self.notify(taskID=taskID)
        if task.isEnabled:
            kwargs = task.functionKwargs()
            result = task.executeFunction(**kwargs)
            if task.variableName and result:
                self.variables[task.variableName] = result
        timerEnd = timer()
        elapsedTime = timerEnd - timerStart
        self.notify(elapsedTime=elapsedTime)
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
            elapsedTime, result = self.executeTask(task, currentTaskID)
            
            if result and task.isJump:
                currentTaskID = int(result)
            else:
                currentTaskID += 1


if __name__ == '__main__':
    engine = MacroEngine()
    engine.loadVariablesMacro(r'C:\python programy\2023_12_12 PyMacro', 'macro.json')
    engine.runProgram()
    engine.saveMacroToFile('saveTest.json')
    engine.saveVariablesToFile('variableSaveTest.json')