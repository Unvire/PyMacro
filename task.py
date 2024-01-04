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
        nameString = f'Task:{self.name}| isEnabled:{self.isEnabled}| '
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
            functionString = f'{self.executeFunction.__globals__["__name__"].split(".")[1]}.{self.executeFunction.__name__}'
        except AttributeError:
            functionString = f'{self.executeFunction}(not imported)'

        parametersDict = {'isJump':self.isJump} if self.isJump else {}
        ## add parameterName: parameterValue to parametersDict
        for parameter in self.parameters:
            parametersDict[parameter] = self.parameters[parameter]

        return {'name':self.name, 'isEnabled':self.isEnabled, 'function':functionString, 
                'parameters':parametersDict, 'saveResultToVariable':self.variableName}
    
    def taskParametersList(self):
        '''
        Returns list of tuples (parameter, parameterValue). 'name' and 'parameters' are skipped. 'parameters' are handled in self.functionArguments.
        Used to display task parameters in table
        '''
        taskDict = self.convertToDict()
        return [(name, taskDict[name]) for name in taskDict if name not in ('parameters',)]
    
    def functionParametersList(self):
        '''
        Returns list of tuples (argument, argumentValue). If argument value is obtained from variables file then argumentValue=variableName
        Used to display function parameters(arguments) in table
        '''
        result = [('isJump', True)] if self.isJump else []
        for argument in self.parameters:
            value = self.parameters[argument]
            if isinstance(value, list):
                valueString = '; '.join([str(val) for val in value])
            else:
                valueString = str(value)
            result.append((argument, valueString))
        return result
    
    def functionKwargs(self):
        '''
        Returns dictionary of function parameters (arguments) key:value. Returns **kwargs that are passed to the function
        '''
        return {parameter:self.parameters[parameter] for parameter in self.parameters}

    def updateParameter(self, isArgument=False, newRecord=('', None)):
        '''
        Updates instance parameters by modifing __dict__. Preserves variableName that value is read from
            isArgument:bool -> True edits self.__dict__['parameters'], False edits self.__dict__
        '''
        keyName, value = newRecord
        if isArgument:
            if keyName == 'isJump':
                self.__setattr__(keyName, value)
            else:
                self.parameters[keyName] = value
        else:
            self.__setattr__(keyName, value)

if __name__ == '__main__':
    task = Task(name='Task test', isEnabled=True, executeFunction='cursorFunctions.moveToCoords', 
                parameters={'coords': 'variable1'}, isJump=True, variableName='')
    print(1, task.convertToDict())
    print(2, task.taskParametersList())
    print(3, task.functionParametersList())
    print(4, task.functionKwargs())
    task.updateParameter(isArgument=True, newRecord=('coords', (0, 600)))
    print(5, task.functionParametersList(), task.functionKwargs())    
    task.updateParameter(isArgument=False, newRecord=('executeFunction', 'aaa'))
    print(6, task.taskParametersList())
