import os, copy, importlib, collections, keyboard
import json
from timeit import default_timer as timer
from datetime import datetime
import task

class MacroEngine():
    def __init__(self):
        '''
        self.taskList: list[tasks] -> list of tasks to be executed in order from 0 to last item
        self.numOfTasks: int -> length of self.taskList
        self.variables: dict -> variables dictionary for program and user
        self.loadedVariables: dict -> deep copy of self.variables, which is saved to file (it avoids saving run time variables)
        self.modules: dict -> dictionary with dynamically imported modules when creating tasks
        self.subscribers: list => list with objects that observe this engine
        self.jumpLabels: dict -> {taskName: ID in self.taskList} used for conditional jumps
        self.undoStack = collections.deque() -> stack that stores 30 previous copies of the self.testList and self.loadedVaribles 
        self.redoStack = collections.deque() -> stack that stores items popped from self.undoStack
        '''
        self.taskList = []
        self.numOfTasks = 0
        self.variables = {}
        self.loadedVariables = {}
        self.modules = {}
        self.subscribers = []
        self.jumpLabels = {}        
        self.undoStack = collections.deque()
        self.redoStack = collections.deque()     
        self.isRun = True   

        item =  [], {}
        self.undoStack.append(item)

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
    
    def _taskListVariablesDeepCopy(self, taskList, variables):
        '''
        Creates deep copy of taskList and Variables. Returns tuple of copied items
        '''
        taskListCopy = copy.deepcopy(taskList)
        variablesCopy = copy.deepcopy(variables)
        return taskListCopy, variablesCopy

    def _saveMacro(self, filePath):
        '''
        Saves self.taskList to file.
            filePath - path where program will save JSON. Must inlcude file name
        '''
        taskDict = {}
        for i, task in enumerate(self.taskList):
            taskDict[str(i)] = task.convertToDict()
        
        with open(filePath, 'w') as file:
            json.dump(taskDict, file, indent=2)
    
    def getTaskList(self):
        '''
        Getter for self.taskList. Returns deep copy of self.taskList
        '''
        return copy.deepcopy(self.taskList)
    
    def setTaskList(self, taskList):
        '''
        Setter for self.taskList
        '''
        self.taskList = taskList

    def clearTaskList(self):
        '''
        Clears self.taskList
        '''
        self.setTaskList([])
    
    def setLoadedVariables(self, variables):
        '''
        Setter for self.loadedVariables
        '''
        self.loadedVariables = variables
    
    def getVariables(self):
        '''
        Getter for self.variables. Returns shallow copy
        '''
        return copy.deepcopy(self.loadedVariables)

    def removeLoadedVariable(self, variableName:str):
        '''
        Removes variableName from self.loadedVariables
        '''
        self.loadedVariables.pop(variableName)
    
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
    
    def strToNum(self, s:str):
        '''
        Converts string to float (decimal point is '.') or int. If it is bot possible returns input value.
        '''
        s = s.strip()
        try:
            if '.' in s: # decimal point
                return float(s)
            else:
                return int(s)
        except ValueError:
            return s
    
    def strToNumList(self, s:str, splitChar=';'):
        '''
        Converts string to list split by splitChar. If it is possible items are converted to float or ints based on presence of decimal point: '.'. 
        Calls self.strToNum for each element
        '''
        result = []
        for item in s.split(splitChar):
            result.append(self.strToNum(item))
        return result

    def loadMacroFile(self, filePath):
        '''
        Opens json file, converts data from dictionary to Task instances and appends them to self.taskList.
            filePath - path to JSON file
        '''
        with open(filePath, 'r') as file:
            taskDict = json.load(file)

        ## convert json to task list
        self.clearTaskList()
        for taskID in taskDict:
            task = self._createTask(taskDict=taskDict[taskID])
            self.taskList.append(task)
            self.numOfTasksGetSet()
        self.clearUndoStack(self.taskList, self.loadedVariables)

    def saveProject(self, filePath):
        '''
        Saves macro project - macro.json, variables and Images. Macro steps are saved with .json extension, variable is saved without extension. The folder Images
        is supposed to store all images used for imageFunctions. Method adds missing .json extension and checks in case of unwanted overwriting (there is a .json in filePath
        with different name) the project is saved in subfolder "New {date of saving}"
            filePath - path of file that will be saved (including filename)
        '''
        if '\\' in filePath:
            *dirPath, macroName = [val for val in filePath.split(os.sep)]
        else:
            *dirPath, macroName = [val for val in filePath.split('/')]
        dirPath = os.sep.join(item for item in dirPath)
    
        ## add extension if it is missing
        if macroName[-5:] != '.json':
            macroName += '.json'

        ## list all '.json' files in dir to check if there is macro already saved
        filesInDir = [fileName for fileName in os.listdir(os.path.join(dirPath)) if fileName[-5:] == '.json']
        if filesInDir:
            for fileName in filesInDir:
                ## if in folder is .json file but names are different then save into new folder. Otherwise overwrite the file
                if fileName != macroName:
                    currentTime = datetime.now().strftime("%d.%m.%Y %H-%M-%S")
                    newFolderName = f'New {currentTime}'                      
                    os.mkdir(os.path.join(dirPath, newFolderName))
                    os.mkdir(os.path.join(dirPath, newFolderName, 'Images'))
                    self._saveMacro(os.path.join(dirPath, newFolderName, macroName))
                    self.saveVariablesToFile(os.path.join(dirPath, newFolderName, 'variables'))
                    return
                
        self._saveMacro(os.path.join(dirPath, macroName))
        self.saveVariablesToFile(os.path.join(dirPath, 'variables'))
        if not os.path.exists(os.path.join(dirPath, 'Images')):
            os.mkdir(os.path.join(dirPath, 'Images'))
    
    def loadVariablesFile(self, filePath):
        '''
        Loads variables from JSON file
        '''
        with open(filePath, 'r') as file:
            self.setLoadedVariables(json.load(file))
    
    def saveVariablesToFile(self, filePath):
        '''
        Saves variable to JSON file (without extension)
        '''
        with open(filePath, 'w') as file:
            json.dump(self.loadedVariables, file, indent=2)
    
    def loadVariablesMacro(self, filePath:str):
        '''
        Loads variables from json and then macro. Both of the files must be in the same directory.
            filePath -> path to the macro .json file
        '''
        if '\\' in filePath:
            *dirPath, macroName = [val for val in filePath.split(os.sep)]
        else:
            *dirPath, macroName = [val for val in filePath.split('/')]

        dirPath = os.sep.join(item for item in dirPath)

        variablesPath = os.path.join(dirPath, 'variables')
        self.loadVariablesFile(variablesPath)

        macroPath = os.path.join(dirPath, macroName)
        self.loadMacroFile(macroPath)
        self.clearUndoStack(self.taskList, self.loadedVariables)
    
    def calculateKwargs(self, kwargs:dict):
        '''
        Replaces function parameters/variables declared in run time with value from self.variables. Works on copy of dictionary
        '''
        kwargsCopy = copy.deepcopy(kwargs)
        for parameterName in kwargsCopy:
            variable = kwargsCopy[parameterName]
            ## replace if value is string
            if isinstance(variable, str): 
                # convert '-variable' to -1 * variable
                sign = 1
                if variable[0] == '-':
                    sign, variable = -1, variable[1:]
                # use value from self.variables
                if variable in self.variables:
                        kwargsCopy[parameterName] = self.variables[variable] * sign
            
            ## replace value if it is in sequence
            elif isinstance(variable, list):
                for i, _ in enumerate(variable[:]):
                    sign = 1
                    # convert '-variable' to -1 * variable
                    if isinstance(variable[i], str) and variable[i][0] == '-':
                        sign, variable[i] = -1, variable[i][1:]
                    # use value from self.variables
                    if variable[i] in self.variables:
                        kwargsCopy[parameterName][i] = self.variables[variable[i]] * sign
        return kwargsCopy

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
        self.variables = copy.deepcopy(self.loadedVariables)
        currentTaskID = 0
        
        ## while loop allows to change currentTaskID programatically (loop back and forward)
        while currentTaskID < self.numOfTasks:
            if keyboard.is_pressed('ctrl+k'):
                break

            task = self.taskList[currentTaskID]
            result = self.executeTask(task, currentTaskID)

            if result and task.isJump:
                currentTaskID = self.jumpLabels[result]
            else:
                currentTaskID += 1
    
    def editTaskParameter(self, taskID=0, taskParameters=(None, None), isArgument=False):
        '''
        Updates selected task from self.taskList.
            taskID: int -> index of item in self.taskList to be edited
            taskParameters:(parameterName:str, val:str, variableName:str) -> parameterName and value is a key:val pair of Task class instance, variableName is key from self.variables
            isArgument: bool -> True edits taskInstance.__dict__['parameters'], False edits taskInstance.__dict__
        '''
        parameterName, parameterValue = taskParameters
        if parameterName == 'function':
            newFunction = self._dynamicImportModule(parameterValue)
            taskParameters = 'executeFunction', newFunction
        elif parameterName == 'saveResultToVariable':
            taskParameters = 'variableName', parameterValue

        self.taskList[taskID].updateParameter(isArgument=isArgument, newRecord=taskParameters)
    
    def deleteTaskFunctionArgument(self, taskID=0, argumentName=None):
        '''
        Removes key:val from taskInstance.parameters dict            
            taskID: int -> index of item in self.taskList to be edited
            argumentName: str -> name of the key to be deleted
        '''
        self.taskList[taskID].deleteFunctionArgument(argumentName)

    def deleteTask(self, taskID:int):
        '''
        Remove task given by ID from self.taskList
        '''
        self.taskList.pop(taskID)

    def newTask(self, index:int):
        '''
        Appends new default task to the list at given index
            index:int
        '''
        taskDict = {'name': 'New task', 'isEnabled': True, 'function': 'synchroFunctions.nothing' , 'parameters': {}, 'saveResultToVariable': ''}
        task = self._createTask(taskDict)
        self.taskList.insert(index, task)
    
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
            currentTask = copy.deepcopy(self.taskList[rowID + i])
            self.taskList.insert(rowID + i, currentTask)
    
    def modifyVariable(self, variable:str, value:str|int|float|list):
        '''
        Updates self.loadedVariables with variable:value pair
        '''
        self.loadedVariables[variable] = value
    
    def clearUndoStack(self, taskList:list, variables:dict):
        '''
        Clears undoStack and appends current item to redoStack.
            item = taskList:list, variablesDict:dict
        '''
        item = self._taskListVariablesDeepCopy(taskList, variables)
        self.undoStack = collections.deque()
        self.redoStack = collections.deque()
        self.undoStack.append(item)
    
    def undoStackPush(self):
        '''
        Makes a deep copy of self.taskList, self.loadedVariables and appends it to the self.undoStack. Clears self.redoStack. Current limit is 30 items. Clears redoStack
        '''
        taskListCopy, variablesCopy = self._taskListVariablesDeepCopy(self.taskList, self.loadedVariables)

        if len(self.undoStack) >= 30:
            self.undoStack.popleft()
        
        pushItem = taskListCopy, variablesCopy
        self.undoStack.append(pushItem)
        self.redoStack = collections.deque()
    
    def undo(self):
        '''
        Undo operation:
        1. Pop item from undoStack and push it into redoStack
        2. Set current state as undoStack[-1] -> set engine state
        3. Refresh window
        '''
        item = self.undoStack.pop()
        self.redoStack.append(item)

        undoTaskList, undoVariables = self.undoStack[-1]
        self.setTaskList(undoTaskList)
        self.setLoadedVariables(undoVariables)
    
    def redo(self):
        '''
        Redo operation:
        1. Pop item from redoStack and push it into undoStack
        2. Set current state as popped item -> set engine state
        3. Refresh window
        '''
        item = self.redoStack.pop()
        taskList, variables = item
        self.undoStack.append(item)
        self.setTaskList(taskList)
        self.setLoadedVariables(variables)
    
    def intendTask(self, IDnum:int):
        '''
        Intends task by adding '   ' (4 spaces) in front of current name.
            IDNum:int -> task index in self.taskList
        '''
        currentTask = self.taskList[IDnum]
        currentTaskName = currentTask.name
        newName = '    ' + currentTaskName
        currentTask.updateParameter(isArgument=False, newRecord=('name', newName))
    
    def unintendTask(self, IDnum:int):
        '''
        Unitends task by removing '   ' (4 spaces) in front of current task name if it is possible (at least 2 spaces are in front).
            IDNum:int -> task index in self.taskList
        '''
        currentTask = self.taskList[IDnum]
        currentTaskName = currentTask.name
        if currentTaskName[:4] == '    ':
            newName = currentTaskName[4:]
            currentTask.updateParameter(isArgument=False, newRecord=('name', newName))


if __name__ == '__main__':
    engine = MacroEngine()
    engine.loadVariablesMacro(r'C:\python programy\2023_12_12 PyMacro\Macros\debug\macro.json')
    print(engine.loadedVariables)
    print(engine.calculateKwargs({'val1':'i'}))
    print(engine.calculateKwargs({'val1':'a'}))
    print(engine.calculateKwargs({'val1':['i', 10]}))
    groups = engine.findGroups([0,1,2, 7,8, 10,11,12, 20])
    print(groups)
    engine.swapTasks(groups, False)
    print(engine.strToNumList('12; 3.20 ;asd'))
    #engine.saveMacroToFile('saveTest.json')

    engine.runProgram()    
    exit()