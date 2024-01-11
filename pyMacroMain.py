import time, os, copy
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
import pyautogui
import macroEngine

class pyMacro(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('PyMacro')

        ## variables
        self.taskList = []
        self.variables = {}
        self.filePath = None
        self.variablesPath = None
        self.macroEngine = macroEngine.MacroEngine()
        self.macroEngine.registerSubscriber(self)
        self.tasksTableChildren = []
        self.isRun = False
        self.clickedTable = None, None
        self.totalTime = 0

        ## frames
        self.mainFrame = ttk.Frame()
        self.rowOneButtonsFrame = ttk.Frame(self.mainFrame)
        self.controlButtonsFrame = ttk.Frame(self.rowOneButtonsFrame)
        self.undoRedoButtonsFrame = ttk.Frame(self.rowOneButtonsFrame)
        self.runButtonsFrame = ttk.Frame(self.rowOneButtonsFrame)
        self.utilityButtonsFrame = ttk.Frame(self.rowOneButtonsFrame)
        self.taskInfoFrame = ttk.Frame(self.mainFrame)
        self.tasksFrame = ttk.Frame(self.mainFrame)
        self.parameterEditFrame = ttk.Frame(self.mainFrame)
        self.taskParametersFrame = ttk.Frame(self.mainFrame)
        self.taskEditButtonsFrame = ttk.Frame(self.mainFrame)

        ## custom style for selection in treeview
        self.selectionGreenStyle = ttk.Style()
        self.selectionGreenStyle.map('selectionGreen.Treeview', background=[('selected', 'green')])

        ## widgets
        # control buttons
        self.newMacroButton = ttk.Button(self.controlButtonsFrame, text='New Macro', command=self.newMacro)
        self.openMacroButton = ttk.Button(self.controlButtonsFrame, text='Open Macro', command=self.openMacroFile)
        self.saveMacroButton = ttk.Button(self.controlButtonsFrame, text='Save Macro', command=self.saveProject)

        # undo redo buttons
        self.undoButton = ttk.Button(self.undoRedoButtonsFrame, text='Undo', command=self.undo)
        self.redoButton = ttk.Button(self.undoRedoButtonsFrame, text='Redo', command=self.redo)

        # run buttons
        self.runButton = ttk.Button(self.runButtonsFrame, text='Run', command=self.runMacro)
        self.killButton = ttk.Button(self.runButtonsFrame, text='Kill', command=...)

        # utility buttons
        self.cursorPositionButton = ttk.Button(self.utilityButtonsFrame, text='Cursor position', command=self.getCursorCoords)

        # task edit buttons
        self.moveTaskUpButton = ttk.Button(self.taskEditButtonsFrame, text='Up', command=lambda: self.moveTask(moveUp=True))
        self.moveTaskDownButton = ttk.Button(self.taskEditButtonsFrame, text='Down', command=lambda: self.moveTask(moveUp=False))
        self.newTaskButton = ttk.Button(self.taskEditButtonsFrame, text='New', command=self.newTask)
        self.copyTaskButton = ttk.Button(self.taskEditButtonsFrame, text='Copy', command=self.duplicateSelectedTasks)
        self.deleteTaskButton = ttk.Button(self.taskEditButtonsFrame, text='Delete', command=self.deleteTask)

        # tasks table
        self.tasksTableTree = ttk.Treeview(self.tasksFrame, columns=('ID', 'Task name', 'Time'), show='headings', selectmode='extended', height=23)        
        self.tasksTableTree.heading('ID', text='ID')
        self.tasksTableTree.heading('Task name', text='Task name')
        self.tasksTableTree.heading('Time', text='Time')
        self.tasksTableTree.column('#1', width=50)
        self.tasksTableTree.column('#2', width=200)
        self.tasksTableTree.column('#3', width=100)

        # taskInfo
        self.infoLabel = ttk.Label(self.taskInfoFrame, text='')

        # parameter edit
        self.parameterNameLabel = ttk.Label(self.parameterEditFrame, text='Name')
        self.parameterNameEntry = ttk.Entry(self.parameterEditFrame)
        self.parameterValueLabel = ttk.Label(self.parameterEditFrame, text='Value')
        self.parameterValueEntry = ttk.Entry(self.parameterEditFrame, width=25)
        self.updateTreeviewParametersButton = ttk.Button(self.parameterEditFrame, text='Update', command=self.updateTreeviewParameters)
        self.deleteArgumentButton = ttk.Button(self.parameterEditFrame, text='Delete', command=self.deleteArgument)

        # task parameters
        self.taskParametersTableTree = ttk.Treeview(self.taskParametersFrame, columns=('Parameter name', 'Value'), show='headings', selectmode='browse', height=4)
        self.taskParametersTableTree.heading('Parameter name', text='Parameter name')
        self.taskParametersTableTree.heading('Value', text='Value')
        self.taskFunctionParametersTableTree = ttk.Treeview(self.taskParametersFrame, columns=('Parameter name', 'Value'), show='headings', selectmode='browse', height=8)
        self.taskFunctionParametersTableTree.heading('Parameter name', text='Argument name')
        self.taskFunctionParametersTableTree.heading('Value', text='Value')
        self.variablesTableTree = ttk.Treeview(self.taskParametersFrame, columns=('Parameter name', 'Value'), show='headings', selectmode='browse', height=8)
        self.variablesTableTree.heading('Parameter name', text='Variable name')
        self.variablesTableTree.heading('Value', text='Value')

        ## widget groups for easier modifing
        self.allButtonsGroup = [self.newMacroButton, self.openMacroButton, self.saveMacroButton, self.undoButton, self.redoButton, self.killButton,
                                self.runButton, self.cursorPositionButton, self.moveTaskUpButton, self.moveTaskDownButton, self.newTaskButton,
                                self.copyTaskButton, self.deleteTaskButton, self.parameterNameEntry, self.parameterValueEntry, 
                                self.updateTreeviewParametersButton, self.deleteArgumentButton]
        self.initButtonsGroup = [self.newMacroButton, self.openMacroButton]

        self.enableAtRunWidgetsGroup = [self.killButton]

        self.undoRedoGroup = [self.undoButton, self.redoButton]

        self.enableTaskListExistGroup = [self.newMacroButton, self.openMacroButton, self.saveMacroButton, self.runButton, self.cursorPositionButton, 
                                         self.newTaskButton]
        
        self.parameterSelectedEnableGroup = [self.parameterValueEntry, self.updateTreeviewParametersButton]
        self.parameterSelectedDisableGroup = [self.parameterNameEntry, self.deleteArgumentButton]
        self.argumentSelectedGroup = [self.parameterNameEntry, self.parameterValueEntry, self.updateTreeviewParametersButton, self.deleteArgumentButton]

        self.taskSelectedEnableGroup = [self.moveTaskUpButton, self.moveTaskDownButton, self.copyTaskButton, self.deleteTaskButton]

        ## position
        # control buttons
        self.newMacroButton.grid(row=0, column=0, padx=(25, 2))
        self.openMacroButton.grid(row=0, column=1, padx=2)
        self.saveMacroButton.grid(row=0, column=2, padx=(2, 25))

        # undo redo buttons
        self.undoButton.grid(row=0, column=0, padx=(25, 2))
        self.redoButton.grid(row=0, column=1, padx=(2, 25))

        # run buttons
        self.runButton.grid(row=0, column=0, padx=(25, 2))
        self.killButton.grid(row=0, column=1, padx=(2, 25))

        # utility buttons
        self.cursorPositionButton.grid(row=0, column=0, padx=25)

        # task edit buttons
        self.moveTaskUpButton.grid(row=0, column=0)
        self.moveTaskDownButton.grid(row=1, column=0)
        self.newTaskButton.grid(row=2, column=0)
        self.copyTaskButton.grid(row=3, column=0)
        self.deleteTaskButton.grid(row=4, column=0)

        # tasks table
        self.infoLabel.grid(row=0, column=0)
        self.tasksTableTree.grid(row=1, column=0)

        # parameter edit
        self.parameterNameLabel.grid(row=0, column=0, padx=2)
        self.parameterNameEntry.grid(row=0, column=1, padx=(2, 10))
        self.parameterValueLabel.grid(row=0, column=2, padx=(10, 2))
        self.parameterValueEntry.grid(row=0, column=3, padx=2)        
        self.deleteArgumentButton.grid(row=1, column=0, columnspan=2)
        self.updateTreeviewParametersButton.grid(row=1, column=2, columnspan=2)

        # task parameters
        self.taskParametersTableTree.grid(row=0, column=0)
        self.taskFunctionParametersTableTree.grid(row=1, column=0, pady=4)
        self.variablesTableTree.grid(row=2, column=0)

        # frames
        # buttons inside first row
        self.controlButtonsFrame.grid(row=0, column=0)
        self.undoRedoButtonsFrame.grid(row=0, column=1)
        self.runButtonsFrame.grid(row=0, column=2)
        self.utilityButtonsFrame.grid(row=0, column=3)
        
        # main layout
        self.rowOneButtonsFrame.grid(row=0, column=0, columnspan=3, pady=5)
        self.taskInfoFrame.grid(row=1, column=1, padx=2)
        self.tasksFrame.grid(row=2, column=1, padx=2)
        self.parameterEditFrame.grid(row=1, column=2, padx=2, pady=5)
        self.taskParametersFrame.grid(row=2, column=2, padx=(2, 5), pady=5)
        self.taskEditButtonsFrame.grid(row=1, column=0, rowspan=2, padx=(5, 2))
        
        self.mainFrame.grid(row=0, column=0)

        ## binds
        self.bind('<ButtonRelease-1>', self.handleMouseClick)
        self.tasksTableTree.bind('<<TreeviewSelect>>', self.taskSelectedEvent)

        self._changeWidgetGroupState('init')

    def _isRunSet(self, state=False):
        '''
        Setter for self.isRun. Handles switching focus styles of self.tasksTableTree.
            state: bool
        '''
        self.isRun = state
        if self.isRun:
            self.tasksTableTree['style'] = 'selectionGreen.Treeview'
            self._changeWidgetGroupState('run')
        else:       
            self.tasksTableTree['style'] = ''
            self._changeWidgetGroupState('taskListExists')
            self._changeUndoRedoButtonsState()
    
    def _clickedTableSet(self, treeview=None, focusedItem=''):
        '''
        Setter for self.clickedTable. Used to verify table of which parameters should be updated. self.clickedTable is reseted (None, None) if self.tasksTableTree is clicked.
            treeview -> ttk.Treeview
            focusedItem:str -> item ID returned by .focus()
        '''
        if treeview in (self.taskParametersTableTree, self.taskFunctionParametersTableTree, self.variablesTableTree):
            self.clickedTable = treeview, focusedItem
        else:
            self.clickedTable = None, None

    def _updateTreeviewRow(self, treeview='', rowID='', columnName='', columnValue=''):
        '''
        Sets value of requested cell in treeview
        '''
        try:
            treeview.set(rowID, column=columnName, value=columnValue)
        except tk.TclError:
            pass

    def _clearTable(self, table):
        ''' 
        Clears ttk.Treeview. 
            table -> ttk.Treeview
        '''
        for item in table.get_children():
            table.delete(item)
    
    def _generateTable(self, table, data):
        ''' 
        Fills ttk.Treeview with data. 
            table -> ttk.Treeview
            data -> list of tuples that are a row in the table
        '''
        for row in data:
            table.insert('', tk.END, values=row)

        if table in (self.taskFunctionParametersTableTree, self.variablesTableTree):
            rowLength = len(data[0]) if data else 2
            table.insert('', tk.END, values=[''] * rowLength) # add empty row in the end
    
    def _handleClickedParameterTreeview(self, treeview):
        '''
        Handles on-click action on parameter treeviews. Gets clicked rowID, updates last clicked treeview and prints focused row data in the Entries.
            treeview: ttk.Treeview
        '''
        _, currentItemID = self._treeviewItemNumber(treeview)                           
        self._clickedTableSet(treeview=treeview, focusedItem=currentItemID)
        parametersDict = treeview.set(currentItemID)
        try:
            self._changeWidgetGroupState('argumentSelected')
            self._updateParameterEntries(parameter=parametersDict['Parameter name'], value=parametersDict['Value'])
        except KeyError:
            pass

        widgetGroupName = self._unselectOtherThan(treeview)
        self._changeWidgetGroupState(widgetGroupName)

    def _clearGenerateTable(self, table, data):
        '''
        Calls self._clearTable and self._generateTable - Clears and fills ttk.Treeview with data. 
            table -> ttk.Treeview
            data -> list of tuples that are a row in the table
        '''
        self._clearTable(table)
        self._generateTable(table, data)
    
    def _treeviewItemNumber(self, treeview):
        '''
        Returns currentItemNumber:num, currentItemID:str of focused item in treeview.
            treeview - ttk.Treeview widget
        '''
        currentItemID = treeview.focus()
        try:
            currentItemNumber = treeview.index(currentItemID)
        except ValueError:
            return None
        return currentItemNumber, currentItemID
    
    def _updateParameterEntries(self, parameter='', value=''):
        '''
        Updates parameter Entries with focused values of Treeviews
            parameter:str
            value:str
        '''
        self.parameterNameEntry.delete(0, tk.END)
        self.parameterValueEntry.delete(0, tk.END)
        self.parameterNameEntry.insert(0, parameter)
        self.parameterValueEntry.insert(0, value)
    
    def _variablesList(self):
        '''
        Converts self.variables dict to [(variableName, value), ...] list
        '''
        variableList = []
        for variable in self.variables:
            if isinstance(self.variables[variable], list):
                row = variable, '; '.join([str(item) for item in self.variables[variable]])
            else:
                row = variable, str(self.variables[variable])
            variableList.append(row)
        return variableList
    
    def _refreshWindow(self):
        '''
        Updates widgets
        '''
        self.update()
        self.update_idletasks()

    def _updateTaskList(self):
        '''
        Updates self.taskist with deep copy from engine
        '''
        self.taskList = self.macroEngine.getTaskList() # copy tasklist
    
    def _changeTaskParameters(self, parameter:str, value:str|int|float|list, isArgument:bool):
        '''
        Helper function for changing task parameters. Task must be selected in order to get number of the row
            parameter -> name of the parameter of the Task instance
            value -> new value of that parameter
            isArgument -> for true task.parameters dict will be modified, for false instance variables will be modified
        ''' 
        ## update Task instance, update local taskList
        currentItemNumber, _ = self._treeviewItemNumber(self.tasksTableTree)
        self.macroEngine.editTaskParameter(taskID=currentItemNumber, taskParameters=(parameter, value), isArgument=isArgument)
        self._updateTaskList()
        self.generateParametersTable(currentItemNumber)
    
    def _modifyVariables(self, variable:str, value:str|int|float|list):
        '''
        Helper function for changing self.loadedVariables of the engine.
            variable -> name of variable
            value -> new value of that variable
        '''
        self.macroEngine.modifyVariable(variable, value)
        self.setVariablesFromEngine()
        variablesList = self._variablesList()
        self._clearGenerateTable(self.variablesTableTree, variablesList)

    def _changeWidgetGroupState(self, widgetGroupName:str):
        '''
        Iterates over widgetGroup and changing state of every item
            widgetGroup -> string name of group. Possibilities:
                'init' - use when initializing program. Only newMacroButton and openMacroButton are enabled
                'taskListExists' - all buttons in rowOneFrame, except killButton
                'run' - macro is running. only kill button is enabled
                'argumentSelected' - item in self.taskFunctionParametersTableTree or self.variablesTableTree is selected
                'parameterSelected' - item in self.taskParametersTableTree is selected
                'taskSelected' - at least one of the items in self.taskTableTree is selected
        '''
        groupDict = {'init': [(self.allButtonsGroup, 'disabled'), (self.initButtonsGroup, 'enabled')],
                     'taskListExists': [(self.allButtonsGroup, 'disabled'), (self.enableTaskListExistGroup, 'enabled')],
                     'run': [(self.allButtonsGroup, 'disabled'), (self.enableAtRunWidgetsGroup, 'enabled')],
                     'argumentSelected': [(self.argumentSelectedGroup, 'enabled')],
                     'parameterSelected': [(self.parameterSelectedEnableGroup, 'enabled'), (self.parameterSelectedDisableGroup, 'readonly')],
                     'taskSelected': [(self.taskSelectedEnableGroup, 'enabled')]}
        
        for groupList in groupDict[widgetGroupName]:
            widgets, state = groupList
            for widget in widgets:
                widget['state'] = state
    
    def _changeUndoRedoButtonsState(self):
        '''
        Changes status of undo and redo buttons. Empty stack means that the button will be disabled
        '''
        statusDict = {True: 'enabled', False: 'disabled'}
        
        undoStatus = len(self.macroEngine.undoStack) > 1
        self.undoButton['state'] = statusDict[undoStatus]
        redoStatus = bool(self.macroEngine.redoStack)
        self.redoButton['state'] = statusDict[redoStatus]
    
    def _unselectOtherThan(self, treeview) -> str:
        '''
        Unselects other treeviews than the one passed as the arguments. Returns widgetGroupName:str
            treeview: ttk.Treeview
        '''
        unselectDict = {self.taskParametersTableTree: [self.taskFunctionParametersTableTree, self.variablesTableTree],
                        self.taskFunctionParametersTableTree: [self.taskParametersTableTree, self.variablesTableTree],
                        self.variablesTableTree: [self.taskFunctionParametersTableTree, self.taskParametersTableTree]}
        widgetGroupNameDict = {self.taskParametersTableTree: 'parameterSelected',
                               self.taskFunctionParametersTableTree: 'argumentSelected',
                               self.variablesTableTree: 'argumentSelected'}
        
        ## unselect
        for widget in unselectDict[treeview]:
            for item in widget.selection():
                widget.selection_remove(item)

        return widgetGroupNameDict[treeview]

    def setVariablesFromEngine(self):
        '''
        Get deep copy of engine's variable dict
        '''
        self.variables = self.macroEngine.getVariables()

    def handleMouseClick(self, event):
        '''
        Handles mouse clicked events. For Treeviews: 
            1. get clicked item data 
            2. generate tables or pass data to Entries
        '''
        ## program is not running and macro exists
        if not self.isRun and self.taskList:
            widget = self.winfo_containing(self.winfo_pointerx(), self.winfo_pointery())
            ## tasks list is clicked 
            if widget == self.tasksTableTree:
                currentItemNumber, _ = self._treeviewItemNumber(self.tasksTableTree)
                self._clickedTableSet(treeview=widget)
                self._updateParameterEntries() # clear entries
                if currentItemNumber is not None:              
                    self.generateParametersTable(currentItemNumber)
            elif widget in (self.taskParametersTableTree, self.taskFunctionParametersTableTree, self.variablesTableTree):
                self._handleClickedParameterTreeview(widget)
    
    def newMacro(self):
        '''
        Creates new Macro - clears taskList and calls self.newTask(). Initialize undoStack and redoStack
        '''
        if self.taskList:
            if not messagebox.askyesno(title='Warning', message='Do you want to create new Macro? Current Macro will be deleted'):
                return
        self.macroEngine.clearTaskList()
        self.newTask()
        self._changeWidgetGroupState('taskListExists')
    
    def openMacroFile(self):
        '''
        Opens macro file and loads variables from the same directory
        '''
        path = os.path.join(os.getcwd(), 'Macros')
        macroFile = filedialog.askopenfilename(title='Open macro', initialdir=path, filetypes=(('Macro file','*.json'),))

        if macroFile:            
            self.filePath = macroFile
            *dirPath, macroName = [val for val in macroFile.split('/')]
            dirPath = '/'.join(item for item in dirPath)
            self.macroEngine.loadVariablesMacro(dirPath, macroName)
            self.setVariablesFromEngine()
            self.generateTasksTable()
            self._changeWidgetGroupState('taskListExists')
    
    def saveProject(self):
        '''
        Saves current project to chosen folder
        '''
        path = os.path.join(os.getcwd(), 'Macros')
        macroFile = filedialog.asksaveasfilename(title='Save macro', initialdir=path, filetypes=(('Macro file','*.json'),))
        
        if macroFile:
            *dirPath, macroName = [val for val in macroFile.split('/')]
            
            ## check if there is .json file in project folder
            dirPath = os.sep.join(item for item in dirPath)

            if macroName[-5:] != '.json':
                macroName += '.json'
            
            filesInDir = [fileName for fileName in os.listdir(os.path.join(dirPath)) if fileName[-5:] == '.json']
            if filesInDir:
                for fileName in filesInDir:
                    ## if in folder is .json file but names are different then save into new folder. Otherwise overwrite the file
                    if fileName != macroName:
                        currentTime = datetime.now().strftime("%d.%m.%Y %H-%M-%S")
                        newFolderName = f'New {currentTime}'                      
                        os.mkdir(os.path.join(dirPath, newFolderName))
                        self.macroEngine.saveMacroToFile(os.path.join(dirPath, newFolderName, macroName))
                        self.macroEngine.saveVariablesToFile(os.path.join(dirPath, newFolderName, 'variables'))
                        return
            
            self.macroEngine.saveMacroToFile(os.path.join(dirPath, macroName))
            self.macroEngine.saveVariablesToFile(os.path.join(dirPath, 'variables'))

    def generateTasksTable(self):
        '''
        Fills tasksTableTree and variablesTableTree with data
        '''
        self._updateTaskList()
        taskNames = [(i, task.name, '') for i, task in enumerate(self.taskList)]
        self.setVariablesFromEngine()
        variablesList = self._variablesList()

        self._clearGenerateTable(self.tasksTableTree, taskNames)
        self._clearGenerateTable(self.variablesTableTree, variablesList)
        self.tasksTableChildren = self.tasksTableTree.get_children()

    def runMacro(self):
        '''
        Executes program
        '''
        if not self.isRun:
            self._isRunSet(True)
            self.generateTasksTable()            
            self.totalTime = 0            
            self.infoLabel['text'] = '0'
            self.macroEngine.runProgram()
        self._isRunSet(False)

    def generateParametersTable(self, taskID=None):
        '''
        Fills taskParametersTableTree and taskFunctionParametersTableTree with data of selected task
            taskID:num - infex of the task in self.tasksTableChildren
        '''
        try:
            task = self.taskList[taskID]
            parameters = task.taskParametersList()
            arguments = task.functionParametersList()

            self._clearGenerateTable(self.taskParametersTableTree, parameters)
            self._clearGenerateTable(self.taskFunctionParametersTableTree, arguments)
        except IndexError:
            pass
    
    def updateWindow(self, taskID=None, elapsedTime=None):
        '''
        Method called by engine with runtime info about current task
            taskID:num - infex of the task in self.tasksTableChildren
            elapsedTime:num - duration of task
        '''
        # select row 
        currentTaskID = self.tasksTableChildren[taskID]
        self.tasksTableTree.focus(currentTaskID)
        self.tasksTableTree.selection_set(currentTaskID)

        ## display elapsed time
        if elapsedTime:
            if elapsedTime != -1:
                self.totalTime += elapsedTime
            self.infoLabel['text'] = f'{self.totalTime:5f}'
            self._updateTreeviewRow(treeview=self.tasksTableTree, rowID=currentTaskID, columnName='Time', columnValue=f'{elapsedTime:5f}')

        self._refreshWindow()
    
    def updateTreeviewParameters(self):
        '''
        Updates task with parameters gained from Entries. 
        1. Get data from Entries
        2. Update Treeviews (update row, clear empty row in the middle, insert empty row)
        3. Convert value to proper type
        '''
        treeview, rowID = self.clickedTable
        isArgument = treeview == self.taskFunctionParametersTableTree
        parameter = self.parameterNameEntry.get()
        value = self.parameterValueEntry.get()

        ## no item selected
        if not treeview:
            return

        ## update tables
        self._updateTreeviewRow(treeview=treeview, rowID=rowID, columnName='Parameter name', columnValue=parameter)
        self._updateTreeviewRow(treeview=treeview, rowID=rowID, columnName='Value', columnValue=value)
        if parameter.lower() == 'name' and not isArgument:
            selectedTaskID = self.tasksTableTree.selection()[0]            
            self._updateTreeviewRow(treeview=self.tasksTableTree, rowID=selectedTaskID, columnName='Task name', columnValue=value)

        ## delete empty row
        if not parameter and not value:
            treeview.delete(rowID)

        ## add empty row as last row, in case that above if-statement cleared last empty row
        lastRow = treeview.get_children()[-1]
        numOfKeys = len(treeview.set(lastRow))
        if treeview.set(lastRow)['Parameter name']:
            treeview.insert('', tk.END, values=[''] * numOfKeys)

        ## convert every single item in list to float or int (if it is possible)
        if ';' in value:
            value = self.macroEngine.strToNumList(value)
        else:
            typeDict = {'false': False, 'true':True}
            if value.lower() in typeDict:
                value = typeDict[value.lower()]
            else:
                value = self.macroEngine.strToNum(value)

        if treeview in (self.taskParametersTableTree, self.taskFunctionParametersTableTree):
            self._changeTaskParameters(parameter, value, isArgument)
        elif treeview is self.variablesTableTree:
            self._modifyVariables(parameter, value)

        self.undoRedoOperation()

    def deleteTask(self):
        '''
        Delete selected task
        '''
        currentID, _ = self._treeviewItemNumber(self.tasksTableTree)
        self.macroEngine.deleteTask(currentID)
        self.generateTasksTable()

        self.undoRedoOperation()
    
    def newTask(self):
        '''
        Creates new task below selected item
        '''
        if self.taskList:
            currentID, _ = self._treeviewItemNumber(self.tasksTableTree)
        else:
            currentID, _ = 0, None
        self.macroEngine.newTask(currentID + 1)
        self.generateTasksTable()

        self.undoRedoOperation()
    
    def moveTask(self, moveUp:bool):
        '''
        Moves selected tasks (rows) in place up or down.
            moveUp: bool -> True = tasks will be moved to the top of the table, False = tasks will be moved to the bottom of the table
        '''
        ## modify self.taskList in place
        rowIDs = [self.tasksTableChildren.index(row) for row in list(self.tasksTableTree.selection())]
        groups = self.macroEngine.findGroups(rowIDs)
        isTableEnd = self.macroEngine.swapTasks(groups, moveUp=moveUp)
        self.generateTasksTable()
        
        ## move selection if tasks were changed, preserve selection if tasks weren't moved
        if not isTableEnd:
            sign = -1 if moveUp else 1
            nameIDs = [self.tasksTableChildren[i + sign] for i in rowIDs]
        else:
            nameIDs = [self.tasksTableChildren[i] for i in rowIDs]
        self.tasksTableTree.selection_set(nameIDs)

        self.undoRedoOperation()
    
    def duplicateSelectedTasks(self):
        '''
        Duplicates selected tasks in place. New task will be inserted after their original
        '''
        rowIDs = [self.tasksTableChildren.index(row) for row in list(self.tasksTableTree.selection())]
        self.macroEngine.duplicateTasks(rowIDs)
        self.generateTasksTable()

        self.undoRedoOperation()
        
    def getCursorCoords(self):
        '''
        Get cursor coords and pixel color
        '''
        self.cursorPositionButton['state'] = 'disabled'
        for i in range(5):
            self.infoLabel['text'] = f'You have {5 - i} seconds to move cursor'
            time.sleep(i)
            self._refreshWindow()
        x, y = pyautogui.position()
        pixelColor = pyautogui.pixel(x, y)
        self.infoLabel['text'] = f'coords: ({x}, {y}) | RGB:{pixelColor}'
        self.cursorPositionButton['state'] = 'enabled'

    def deleteArgument(self):
        '''
        Removes chosen function argument
        '''
        argumentName = self.parameterNameEntry.get()
        treeview, rowID = self.clickedTable

        ## verify that clicked treeview is the one with function arguments
        if treeview != self.taskFunctionParametersTableTree:
            return
        
        decision = messagebox.askyesno('Confirmation', message=f"Do you want to delete {argumentName} from task's argument")
        if decision: 
            ## delete row unless it is the last one
            lastRow = treeview.get_children()[-1]
            if rowID != lastRow:
                treeview.delete(rowID)
            
            ## remove parameter
            currentItemNumber, _ = self._treeviewItemNumber(self.tasksTableTree)
            self.macroEngine.deleteTaskFunctionArgument(taskID=currentItemNumber, argumentName=argumentName)
            self._updateTaskList()

            self.undoRedoOperation()
    
    def undo(self):
        '''
        Perform undo operation and refresh the window
        '''
        self.macroEngine.undo()
        self.generateTasksTable()
        ## to be fixed   
        if self.clickedTable[0]:
            currentItemNumber, _ = self._treeviewItemNumber(self.tasksTableTree)
            self.generateParametersTable(currentItemNumber)
        self._changeUndoRedoButtonsState()
        self._refreshWindow()

    def redo(self):
        '''
        Perform redo operation and refresh the window
        '''
        self.macroEngine.redo()
        self.generateTasksTable()     
        ## to be fixed   
        if self.clickedTable[0]:
            currentItemNumber, _ = self._treeviewItemNumber(self.tasksTableTree)
            self.generateParametersTable(currentItemNumber)        
        self._changeUndoRedoButtonsState()
        self._refreshWindow()
    
    def taskSelectedEvent(self, event):
        if not self.isRun:
            self._changeWidgetGroupState('taskSelected')
    
    def undoRedoOperation(self):
        '''
        Function for handling undo and redo. Pushes current state to undoStack and updates state of the buttons
        '''
        self.macroEngine.undoStackPush()
        self._changeUndoRedoButtonsState()

if __name__ == '__main__':
    app = pyMacro()
    app.mainloop()