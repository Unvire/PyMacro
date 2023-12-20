import os
import json
from timeit import default_timer as timer
import importlib

class Task:
    def __init__(self, name='', isEnabled=False, executeFunction=None, parameters=None, isJump=False, variableName=''):
        '''
        name: str -> name of the task
        isEnabled: bool -> disabled task are not executed
        executeFunction -> reference for function to be executed
        parameters: dict -> dictionary of parameters, that are passed as keyword arguments to executeFunction. Each parameter is a tuple: (value, variableName)
        isJump: bool -> parameter of "logicFunctions.checkCondition". Program will jump to taskID=resultTrue or taskID=resultFalse after evaluating condition
        variableName:str -> name of the variable that will store output of function. Function must return something (bool(result)==True) and variable name must be any string
        '''
        self.name = name
        self.isEnabled = isEnabled
        self.executeFunction = executeFunction
        self.parameters =  parameters
        self.isJump = isJump
        self.variableName = variableName

    def __str__(self):
        nameString = f'Task:{self.name}| state:{self.isEnabled}| '
        try:
            functionString = f'function:{self.executeFunction.__name__}, package:{self.executeFunction.__globals__["__name__"]}| '
        except AttributeError:
            functionString = f'{self.executeFunction}(not imported)| '
        parametersString = f'parameters:{self.parameters}, isJump:{self.isJump}, variableName:{self.variableName}'
        return nameString + functionString + parametersString

    def convertToDict(self):
        '''
        Returns dictionary representation. Used to saving task list into json file
        '''
        try:
            functionString = f'{self.executeFunction.__globals__["__name__"]}.{self.executeFunction.__name__}'
        except AttributeError:
            functionString = f'{self.executeFunction}(not imported)'

        parametersDict = {}
        ## get parameter:variableName if variableName exists else parameter:value
        for parameter in self.parameters:
            parameterValue = self.parameters[parameter][1] if self.parameters[parameter][1] else self.parameters[parameter][0]
            parametersDict[parameter] = parameterValue
        
        return {'name':self.name, 'enabled':self.isEnabled, 'function':functionString, 'isJump':self.isJump, 
                'parameters':parametersDict, 'saveResultToVariable':self.variableName}
    
    def taskParametersList(self):
        '''
        Returns list of tuples (parameter, parameterValue). 'name' and 'parameters' are skipped. 'parameters' are handled in self.functionArguments.
        Used to display task parameters in table
        '''
        taskDict = self.convertToDict()
        return [(name, taskDict[name]) for name in taskDict if name not in ('name', 'parameters')]
    
    def functionParametersList(self):
        '''
        Returns list of tuples (argument, argumentValue). If argument value is obtained from variables file then argumentValue=variableName
        Used to display function parameters(arguments) in table
        '''
        result = []
        for argument in self.parameters:
            value, variableName = self.parameters[argument]
            if variableName:
                valueString = variableName
            elif isinstance(value, list):
                valueString = '; '.join([str(val) for val in value])
            else:
                valueString = str(value)
            result.append((argument, valueString))
        return result
    
    def functionKwargs(self):
        '''
        Returns dictionary of function parameters (arguments) key:value. Returns **kwargs that are passed to the function
        '''
        return {parameter:self.parameters[parameter][0] for parameter in self.parameters}


class MacroEngine():
    def __init__(self):
        '''
        self.taskList: list[tasks] -> list of tasks to be executed in order from 0 to last item
        self.numOfTasks: int -> length of self.taskList
        self.variables: dict -> variables dictionary for program and user
        self.modules: dict -> dictionary with dynamically imported modules when creating tasks
        '''
        self.taskList = []
        self.numOfTasks = 0
        self.variables = {}
        self.modules = {}

    def numOfTasksGetSet(self):
        '''
        Getter and setter of self.numOfTasks
        '''
        self.numOfTasks = len(self.taskList)
        return self.numOfTasks

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

        
        print(variableName)
        taskInstance = Task(name=name, isEnabled=isEnabled, executeFunction=taskFunction, parameters=parameters, isJump=isJump, variableName=variableName)
        return taskInstance
        

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

    def executeTask(self, task):
        '''
        Executes task by calling function in task.executeFunction with keyword arguments given in task.parameters. Returns time of execution and result of task
            task: instance of Task class
        '''
        timerStart = timer()
        if task.isEnabled:
            kwargs = task.functionKwargs()
            result = task.executeFunction(**kwargs)
            if task.variableName and result:
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
            
            if result and task.isJump:
                currentTaskID = int(result)
            else:
                currentTaskID += 1


if __name__ == '__main__':
    task = Task(name='Task test', isEnabled=True, executeFunction='cursorFunctions.moveToCoords', 
                parameters={'coords':((300, 500), 'variable1')}, isJump=False, variableName='')
    print(task.convertToDict())
    print(task.taskParametersList())
    print(task.functionParametersList())
    print(task.functionKwargs())

    engine = MacroEngine()
    engine.loadVariablesMacro(r'C:\python programy\2023_12_12 PyMacro', 'macro.json')
    engine.runProgram()
    engine.saveMacroToFile('saveTest.json')
    engine.saveVariablesToFile('variableSaveTest.json')