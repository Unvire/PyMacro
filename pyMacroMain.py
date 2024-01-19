import time, os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ttkwidgets.autocomplete import AutocompleteEntry
from idlelib.tooltip import Hovertip
import pyautogui
import macroEngine
import allFunctions

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

        ## autocomplete list:
        autocompleteParameters, autocompleteValues = allFunctions.getFunctionNames()

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
        self.killButton = ttk.Button(self.runButtonsFrame, text='Kill', command=self.stopMacro)

        # utility buttons
        self.cursorPositionButton = ttk.Button(self.utilityButtonsFrame, text='Cursor position', command=self.getCursorCoords)

        # task edit buttons
        self.moveTaskUpButton = ttk.Button(self.taskEditButtonsFrame, text='Up', command=lambda: self.moveTask(moveUp=True))
        self.moveTaskDownButton = ttk.Button(self.taskEditButtonsFrame, text='Down', command=lambda: self.moveTask(moveUp=False))
        self.newTaskButton = ttk.Button(self.taskEditButtonsFrame, text='New', command=self.newTask)
        self.copyTaskButton = ttk.Button(self.taskEditButtonsFrame, text='Copy', command=self.duplicateSelectedTasks)
        self.deleteTaskButton = ttk.Button(self.taskEditButtonsFrame, text='Delete', command=self.deleteTask)
        self.intendButton = ttk.Button(self.taskEditButtonsFrame, text='Intend', command=self.intend)
        self.unintendButton = ttk.Button(self.taskEditButtonsFrame, text='Unintend', command=self.unintend)

        # tasks table
        self.tasksTableTree = ttk.Treeview(self.tasksFrame, columns=('ID', 'Task name', 'Result variable', 'Time'), show='headings', selectmode='extended', height=23)        
        self.tasksTableTree.heading('ID', text='ID')
        self.tasksTableTree.heading('Task name', text='Task name')
        self.tasksTableTree.heading('Result variable', text='Result variable')
        self.tasksTableTree.heading('Time', text='Time')
        self.tasksTableTree.column('#1', width=30)
        self.tasksTableTree.column('#2', width=200)
        self.tasksTableTree.column('#3', width=100)
        self.tasksTableTree.column('#4', width=100)

        # taskInfo
        self.infoLabel = ttk.Label(self.taskInfoFrame, text='')

        # parameter edit
        self.parameterNameLabel = ttk.Label(self.parameterEditFrame, text='Name')
        self.parameterNameEntry = AutocompleteEntry(self.parameterEditFrame, completevalues=autocompleteParameters)
        self.parameterValueLabel = ttk.Label(self.parameterEditFrame, text='Value')
        self.parameterValueEntry = AutocompleteEntry(self.parameterEditFrame, width=25, completevalues=autocompleteValues)
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
                                self.updateTreeviewParametersButton, self.deleteArgumentButton, self.intendButton, self.unintendButton]
        self.initButtonsGroup = [self.newMacroButton, self.openMacroButton]

        self.enableAtRunWidgetsGroup = [self.killButton]

        self.undoRedoGroup = [self.undoButton, self.redoButton]

        self.enableTaskListExistGroup = [self.newMacroButton, self.openMacroButton, self.saveMacroButton, self.runButton, self.cursorPositionButton, 
                                         self.newTaskButton]

        self.parameterSelectedEnableGroup = [self.parameterValueEntry, self.updateTreeviewParametersButton]
        self.parameterSelectedDisableGroup = [self.parameterNameEntry, self.deleteArgumentButton]
        self.argumentSelectedGroup = [self.parameterNameEntry, self.parameterValueEntry, self.updateTreeviewParametersButton, self.deleteArgumentButton]

        self.taskSelectedEnableGroup = [self.moveTaskUpButton, self.moveTaskDownButton, self.copyTaskButton, self.deleteTaskButton, self.intendButton, 
                                        self.unintendButton]

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
        self.intendButton.grid(row=5, column=0)
        self.unintendButton.grid(row=6, column=0)

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

        ## hover tips
        #first row buttons
        self.newMacroButtonHovertip = Hovertip(self.newMacroButton, 'Create new macro')
        self.openMacroButtonHovertip = Hovertip(self.openMacroButton, 'Open exisitng macro')
        self.saveMacroButtonHovertip = Hovertip(self.saveMacroButton, 'Save project')
        self.undoButtonHovertip = Hovertip(self.undoButton, 'Undo previous modification')
        self.redoButtonHovertip = Hovertip(self.redoButton, 'Revert undo')
        self.runButtonHovertip = Hovertip(self.runButton, 'Run macro')
        self.killButtonHovertip = Hovertip(self.killButton, 'Stop macro | ctrl + k')
        self.cursorPositionButtonHovertip = Hovertip(self.cursorPositionButton, 'Prints cursor position(x,y) and color(R, G, B) after 5 second ')

        # task edit buttons
        self.moveTaskUpButtonHovertip = Hovertip(self.moveTaskUpButton, 'Move selected tasks up the list (multi selection with ctrl)')
        self.moveTaskDownButtonHovertip = Hovertip(self.moveTaskDownButton, 'Move selected tasks down the list (multi selection with ctrl)')
        self.newTaskButtonHovertip = Hovertip(self.newTaskButton, 'Inserts new task below current selected item')
        self.copyTaskButtonHovertip = Hovertip(self.copyTaskButton, 'Duplicates selected tasks (multi selection with ctrl)')
        self.deleteTaskButtonHovertip = Hovertip(self.deleteTaskButton, 'Delete selected task')
        self.intendButtonHovertip = Hovertip(self.intendButton, 'Adds 4 spaces in the begining of the task name')
        self.unintendButtonHovertip = Hovertip(self.unintendButton, 'Removes 4 spaces in the begining of the task name')

        # edit task parameters
        self.parameterNameEntryHovertip = Hovertip(self.parameterNameEntry, 'Write name of the parameter')
        self.parameterValueEntryHovertip = Hovertip(self.parameterValueEntry, 'Write value of the parameter. Items of list must be separated with ";". All numbers are converted to ints or floats')
        self.updateTreeviewParametersButtonHovertip = Hovertip(self.updateTreeviewParametersButton, 'Confirm written values and modify selected parameter')
        self.deleteArgumentButtonHovertip = Hovertip(self.deleteArgumentButton, 'Delete selected parameter')

        # treeviews
        self.tasksTableTreeHovertip = Hovertip(self.tasksTableTree, 'Table with list of the tasks. Run time variables and elapsed time is displayed in dedicated columns')
        self.taskParametersTableTreeHovertip = Hovertip(self.taskParametersTableTree, 'Table with list of common parameters')
        self.taskFunctionParametersTableTreeHovertip = Hovertip(self.taskFunctionParametersTableTree, 'Table with list of parameters dedicated to function')
        self.variablesTableTreeHovertip = Hovertip(self.variablesTableTree, 'Table with list of the variables that will be saved to file')
        
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
                'taskListExists' - all buttons in rowOneFrame, except killButton. Disables editing task parameters widgets
                'run' - macro is running. only kill button is enabled
                'argumentSelected' - item in self.taskFunctionParametersTableTree or self.variablesTableTree is selected
                'parameterSelected' - item in self.taskParametersTableTree is selected
                'taskSelected' - at least one of the items in self.taskTableTree is selected
        '''
        groupDict = {'init': [(self.allButtonsGroup, 'disabled'), (self.initButtonsGroup, 'enabled')],
                     'taskListExists': [(self.allButtonsGroup, 'disabled'), (self.enableTaskListExistGroup, 'enabled'), (self.argumentSelectedGroup, 'disabled')],
                     'run': [(self.allButtonsGroup, 'disabled'), (self.enableAtRunWidgetsGroup, 'enabled')],
                     'argumentSelected': [(self.argumentSelectedGroup, 'enabled')],
                     'parameterSelected': [(self.parameterSelectedEnableGroup, 'enabled'), (self.parameterSelectedDisableGroup, 'readonly')],
                     'taskSelected': [(self.taskSelectedEnableGroup, 'enabled'), (self.argumentSelectedGroup, 'disabled')]}
        
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

    def _getSelectedRowNumbers(self):
        '''
        Return list of selected row ID numbers ([0, 1, 2, 3... ])
        '''
        return [self.tasksTableChildren.index(row) for row in list(self.tasksTableTree.selection())]

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
        self.infoLabel['text'] = ''
        self.title('PyMacro')
    
    def openMacroFile(self):
        '''
        Opens macro file and loads variables from the same directory
        '''
        path = os.path.join(os.getcwd(), 'Macros')
        macroFile = filedialog.askopenfilename(title='Open macro', initialdir=path, filetypes=(('Macro file','*.json'),))

        if macroFile:            
            self.filePath = macroFile
            self.macroEngine.loadVariablesMacro(macroFile)
            self.setVariablesFromEngine()
            self.generateTasksTable()
            self._changeWidgetGroupState('taskListExists')
            self.infoLabel['text'] = ''
            *_, macroName = [val for val in macroFile.split('/')]
            self.title('PyMacro - ' + macroName)
    
    def saveProject(self):
        '''
        Saves current project to chosen folder
        '''
        path = os.path.join(os.getcwd(), 'Macros')
        macroFile = filedialog.asksaveasfilename(title='Save macro', initialdir=path, filetypes=(('Macro file','*.json'),))
        
        if macroFile:
            self.macroEngine.saveProject(macroFile)            
            *_, macroName = [val for val in macroFile.split('/')]
            self.title('PyMacro - ' + macroName)

    def generateTasksTable(self):
        '''
        Fills tasksTableTree and variablesTableTree with data
        '''
        self._updateTaskList()
        taskNames = [(i, task.name, task.variableName, '') for i, task in enumerate(self.taskList)]
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
            try:
                self.macroEngine.runProgram()
            except Exception as e:
                messagebox.showerror(title='Error', message=e)
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

        coulmnNamesDict = {'name': 'Task name', 'saveResultToVariable': 'Result variable'}
        if parameter in ('name', 'saveResultToVariable') and not isArgument:
            selectedTaskID = self.tasksTableTree.selection()[0]            
            self._updateTreeviewRow(treeview=self.tasksTableTree, rowID=selectedTaskID, columnName=coulmnNamesDict[parameter], columnValue=value)

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

        self.generateTasksTable()
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
        rowIDs = self._getSelectedRowNumbers()
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
            self._refreshWindow()
            time.sleep(1)
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
        if treeview not in (self.taskFunctionParametersTableTree, self.variablesTableTree):
            return
        
        decision = messagebox.askyesno('Confirmation', message=f"Do you want to delete {argumentName} from task's argument")
        if decision: 
            ## delete row unless it is the last one
            lastRow = treeview.get_children()[-1]
            if rowID != lastRow:
                treeview.delete(rowID)
            
            ## remove variable or parameter
            if treeview is self.variablesTableTree:
                self.macroEngine.removeLoadedVariable(argumentName)
            else:
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
            self._changeWidgetGroupState('argumentSelected')
            self._updateParameterEntries() # clear entries
            self._changeWidgetGroupState('taskSelected')
    
    def undoRedoOperation(self):
        '''
        Function for handling undo and redo. Pushes current state to undoStack and updates state of the buttons
        '''
        self.macroEngine.undoStackPush()
        self._changeUndoRedoButtonsState()
    
    def stopMacro(self):
        '''
        Sets engine.isRun to False 
        '''
        self.macroEngine.isRun = False
        self._isRunSet(False)
    
    def intend(self):
        '''
        Adds 2 spaces before each selected task name
        '''
        rowIDs = self._getSelectedRowNumbers()
        for IDnum in rowIDs:
            self.macroEngine.intendTask(IDnum)

        self.generateTasksTable()
        self.undoRedoOperation()
        nameIDs = [self.tasksTableChildren[i] for i in rowIDs]
        self.tasksTableTree.selection_set(nameIDs)
        

    def unintend(self):
        '''
        Removes 2 spaces before each selected task name, if it is possible
        '''
        rowIDs = self._getSelectedRowNumbers()
        for IDnum in rowIDs:
            self.macroEngine.unintendTask(IDnum)
        
        self.generateTasksTable()
        self.undoRedoOperation()
        nameIDs = [self.tasksTableChildren[i] for i in rowIDs]
        self.tasksTableTree.selection_set(nameIDs)

if __name__ == '__main__':
    app = pyMacro()
    app.mainloop()