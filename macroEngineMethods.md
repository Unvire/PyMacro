## Each method is described in the macroEngine.py. Below there are listed all the method split into 'theme' groups
** Setters **
- setTaskList(self, taskList)
- clearTaskList(self)
- setLoadedVariables(self, variables)
- numOfTasksGetSet(self)

** getters **
- getTaskList(self)
- getVariables(self)

** creating task **
- _createTask(self, taskDict=None)
- _dynamicImportModule(self, packageString:str)

** save project **
- _saveMacro(self, filePath)
- saveVariablesToFile(self, filePath)
- saveProject(self, filePath)

** load project **
- loadMacroFile(self, filePath)
- loadVariablesFile(self, filePath)
- loadVariablesMacro(self, filePath:str)

** run macro **
- calculateKwargs(self, kwargs:dict)
- executeTask(self, task, taskID)
- runProgram(self)

** edit task and variables **
- removeLoadedVariable(self, variableName:str)
- editTaskParameter(self, taskID=0, taskParameters=(None, None), isArgument=False)
- deleteTaskFunctionArgument(self, taskID=0, argumentName=None)
- modifyVariable(self, variable:str, value:str|int|float|list)
- intendTask(self, IDnum:int)
- unintendTask(self, IDnum:int)

** handling tasklist **
- _updateJumpLabels(self)
- deleteTask(self, taskID:int)
- newTask(self, index:int)
- swapTasks(self, groups, moveUp=True) -> bool
- duplicateTasks(self, rowIDs)

** undo and redo **
- _taskListVariablesDeepCopy(self, taskList, variables)
- clearUndoStack(self, taskList:list, variables:dict)
- undoStackPush(self)
- undo(self)
- redo(self)

** observer **
- registerSubscriber(self, subscriber)
- notify(self, taskID=None, elapsedTime=None)

** calculations **
- strToNum(self, s:str)
- strToNumList(self, s:str, splitChar=';')
- findGroups(self, rowIDs=[]) -> [[int, int]]