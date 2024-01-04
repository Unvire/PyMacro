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
        self.jumpLabels: dict -> {taskName: ID in self.taskList} used for conditional jumps
        '''
        self.taskList = []
        self.numOfTasks = 0
        self.variables = {}
        self.modules = {}
        self.subscribers = []
        self.jumpLabels = {}

    def _dynamicImportModule(self, packageString:str):
        '''
        Import dynamically function from module inside 'functions' package. Returns reference to that function
            packageString:str -> moduleName.functionName, for example: "cursorFunctions.moveToCoords" 
        '''
        ## get module and function by their string name
        packageName, taskName = packageString.split('.')  
        packageName = '.' + packageName

        ## import package from functions folder
        if packageName not in self.modules:
            self.modules[packageName] = importlib.import_module(packageName, package='functions')
        
        ## get requested function from that package
        taskFunction = getattr(self.modules[packageName], taskName)
        return taskFunction

    def _createTask(self, taskDict=None):
        '''
        Converts taskDict to instance of Task class. Returns instance of Task class
        '''
        name = taskDict['name']
        isEnabled = taskDict['isEnabled']
        parameters = taskDict['parameters']        
        variableName = taskDict['saveResultToVariable']
        taskFunction = self._dynamicImportModule(taskDict['function'])
        
        ## check if task is a conditional jump and remove it from parameters dict
        if 'checkCondition' in taskDict['function'] and 'isJump' in parameters:
            isJump = parameters['isJump']
            parameters.pop('isJump')
        else:            
            isJump = False

        taskInstance = task.Task(name=name, isEnabled=isEnabled, executeFunction=taskFunction, parameters=parameters, isJump=isJump, variableName=variableName)
        return taskInstance
    
    def _updateJumpLabels(self):
        '''
        Updates self.jumpLabels {taskName:ID in self.taskList} in place
        '''
        self.jumpLabels = {task.name:i for i, task in enumerate(self.taskList)}
    
    def getTaskList(self):
        '''
        Getter for self.taskList. Returns shallow copy of self.taskList
        '''
        return [task for task in self.taskList]

    def clearTaskList(self):
        '''
        Clears self.taskList
        '''
        self.taskList = []
    
    def getVariables(self):
        '''
        Getter for self.variables. Returns shallow copy
        '''
        return self.variables.copy()
    
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
            subscriber.updateWindow(taskID=taskID, elapsedTime=elapsedTime)
    

    def loadMacroFile(self, filePath):
        '''
        Opens json file, converts data from dictionary to Task instances and appends them to self.taskList.
            filePath - path to JSON file
        '''
        with open(filePath, 'r') as file:
            taskDict = json.load(file)

        ## convert json to task list
        self.taskList = []
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
        variablesPath = os.path.join(dirPath, 'variables')
        self.loadVariablesFile(variablesPath)
        macroPath = os.path.join(dirPath, fileName)
        self.loadMacroFile(macroPath)
    
    def calculateKwargs(self, kwargs:dict):
        '''
        Replaces variables declared in run time with value from self.variables
        '''
        for parameterName in kwargs:
            variable = kwargs[parameterName]
            ## replace if value is string
            if isinstance(variable, str) and variable in self.variables:
                kwargs[parameterName] = self.variables[variable]
            
            ## replace value if it is in sequence
            elif isinstance(variable, list):
                for i, _ in enumerate(variable):
                    if isinstance(variable[i], str) and variable[i] in self.variables:
                        kwargs[parameterName][i] = self.variables[variable[i]]
        return kwargs

    def executeTask(self, task, taskID):
        '''
        Executes task by calling function in task.executeFunction with keyword arguments given in task.parameters. Returns time of execution and result of task
            task: instance of Task class
        '''
        timerStart = timer()
        self.notify(taskID=taskID)
        result, elapsedTime = None, -1
        if task.isEnabled:
            kwargs = self.calculateKwargs(task.functionKwargs())
            result = task.executeFunction(**kwargs)
            if task.variableName and result is not None:
                self.variables[task.variableName] = result
            timerEnd = timer()
            elapsedTime = timerEnd - timerStart
        self.notify(taskID=taskID, elapsedTime=elapsedTime)
        return result
    
    def runProgram(self):
        '''
        Runs macro by iterating over self.taskList and executing task
        '''
        self.numOfTasksGetSet()
        self._updateJumpLabels()
        currentTaskID = 0
        
        ## while loop allows to change currentTaskID programatically (loop back and forward)
        while currentTaskID < self.numOfTasks:
            task = self.taskList[currentTaskID]
            result = self.executeTask(task, currentTaskID)

            if result and task.isJump:
                currentTaskID = self.jumpLabels[result]
            else:
                currentTaskID += 1
    
    def editTaskParameter(self, taskID=0, taskParameters=(None, None, None), isArgument=False):
        '''
        Updates selected task from self.taskList.
            taskID: int -> index of item in self.taskList to be edited
            taskParameters:(parameterName:str, val:str, variableName:str) -> parameterName and value is a key:val pair of Task class instance, variableName is key from self.variables
            isArgument: bool -> True edits taskInstance.__dict__['parameters'], False edits taskInstance.__dict__
        '''
        parameterName, parameterValue, parameterVariable = taskParameters
        if parameterName == 'function':
            newFunction = self._dynamicImportModule(parameterValue)
            taskParameters = 'executeFunction', newFunction, None
        elif parameterName == 'saveResultToVariable':
            taskParameters = 'variableName', parameterValue, None

        self.taskList[taskID].updateParameter(isArgument=isArgument, newRecord=taskParameters)

    def deleteTask(self, taskID:int):
        '''
        Remove task given by ID from self.taskList
        '''
        self.taskList.pop(taskID)

    def newTask(self):
        '''
        Appends new default task to the list
        '''
        taskDict = {'name': 'New task', 'isEnabled': True, 'function': 'cursorFunctions.moveToCoords' , 'parameters': {}, 'saveResultToVariable': ''}
        task = self._createTask(taskDict)
        self.taskList.append(task)
    
    def findGroups(self, rowIDs=[]) -> [[int, int]]:
        '''
        Helper function for rearranging tasks. Converts list of selected rowIDs to groups -> list of [firstID, numOfConsecutiveElements] lists.
        Example [1,2,3, 6,7, 10,11, 20] -> [[1,3], [6,2], [10,2], 20]
            rowIDs -> list of rowIDs. Can be unsorted.
        '''
        rowIDs = sorted(rowIDs)
        stack = [rowIDs.pop(0)]
        groups = []
        while rowIDs:            
            currentID = rowIDs.pop(0)
            if currentID == stack[-1] + 1:
                stack.append(currentID)
            else:
                groups.append([stack[0], len(stack)])
                stack = [currentID]
        if stack:
            groups.append([stack[0], len(stack)])
        return groups
    
    def swapTasks(self, groups, moveUp=True) -> bool:
        '''
        Swaps tasks in place. Returns if end of the table is reached.
            groups -> result of self.findGroups
            moveUp: bool -> if True then task 2 will be swapped with 1, if False then task 2 will be swapped with 3
        '''
        ## check if last item + group length will be outside the table (index < 0)
        if moveUp and groups[0][0] - 1 < 0:
            return True
        
        ## check if last item + group length will be outside the table (index > len(self.taskList). 
        # (index + length - 1) + 1 > len(self.taskList) - 1 ---> index + length + 1 > len(self.taskList)
        if not moveUp and groups[-1][0] + groups[-1][1] + 1 > len(self.taskList):
            return True
        
        ## swap in place items (smaller index first for move up, bigger index first for move down)
        signedOne = -1 if moveUp else 1
        for group in groups:
            initialIndex, groupLength = group
            indexesRange = range(initialIndex, initialIndex + groupLength) if moveUp else range(initialIndex + groupLength - 1, initialIndex - 1, -1)
            for i in indexesRange:
                iOrigin = i
                iTarget = i + signedOne
                self.taskList[iOrigin],  self.taskList[iTarget] = self.taskList[iTarget],  self.taskList[iOrigin]
        return False

    def duplicateTasks(self, rowIDs):
        '''
        Duplicates selected tasks in place. New task will be inserted after their original
        '''
        rowIDs = sorted(rowIDs)
        for i, rowID in enumerate(rowIDs):
            currentTask = self.taskList[rowID + i]
            self.taskList.insert(rowID + i, currentTask)


if __name__ == '__main__':
    engine = MacroEngine()
    engine.loadVariablesMacro(r'C:\python programy\2023_12_12 PyMacro\Macros\debug', 'macro.json')
    engine.variables['i'] = 0
    print(engine.calculateKwargs({'val1':'i'}))
    print(engine.calculateKwargs({'val1':'a'}))
    print(engine.calculateKwargs({'val1':['i', 10]}))
    groups = engine.findGroups([0,1,2, 7,8, 10,11,12, 20])
    print(groups)
    engine.swapTasks(groups, False)
    
    engine.saveMacroToFile('saveTest.json')

    engine.runProgram()
    engine.saveVariablesToFile('variableSaveTest')