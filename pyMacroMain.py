import time
import os
import tkinter as tk
from tkinter import ttk, filedialog
import pyautogui
import macroEngine

class pyMacro(tk.Tk):
    def __init__(self):
        super().__init__()

        ## variables
        self.tasksList = []
        self.variables = {}
        self.filePath = None
        self.variablesPath = None
        self.macroEngine = macroEngine.MacroEngine()
        self.macroEngine.registerSubscriber(self)
        self.tasksTableChildren = []
        self.isRun = False
        self.clickedTable = None, None

        ## frames
        self.mainFrame = ttk.Frame()
        self.rowOneButtonsFrame = ttk.Frame(self.mainFrame)
        self.controlButtonsFrame = ttk.Frame(self.rowOneButtonsFrame)
        self.runButtonsFrame = ttk.Frame(self.rowOneButtonsFrame)
        self.utilityButtonsFrame = ttk.Frame(self.rowOneButtonsFrame)
        self.parameterEditFrame = ttk.Frame(self.mainFrame)
        self.tasksFrame = ttk.Frame(self.mainFrame)
        self.taskParametersFrame = ttk.Frame(self.mainFrame)
        self.taskEditButtonsFrame = ttk.Frame(self.mainFrame)

        ## custom style for selection in treeview
        self.selectionGreenStyle = ttk.Style()
        self.selectionGreenStyle.map('selectionGreen.Treeview', background=[('selected', 'green')])

        ## widgets
        # control buttons
        self.newMacroButton = ttk.Button(self.controlButtonsFrame, text='New Macro', command=...)
        self.openMacroButton = ttk.Button(self.controlButtonsFrame, text='Open Macro', command=self.openMacroFile)
        self.saveMacroButton = ttk.Button(self.controlButtonsFrame, text='Save Macro', command=...)
        self.settingsButton = ttk.Button(self.controlButtonsFrame, text='Settings', command=...)

        # run buttons
        self.runButton = ttk.Button(self.runButtonsFrame, text='Run', command=self.runMacro)
        self.killButton = ttk.Button(self.runButtonsFrame, text='Kill', command=...)

        # utility buttons
        self.cursorPositionButton = ttk.Button(self.utilityButtonsFrame, text='Cursor position', command=self.getCursorCoords)
        self.variablesButton = ttk.Button(self.utilityButtonsFrame, text='Variables', command=...)

        # task edit buttons
        self.moveTaskUpButton = ttk.Button(self.taskEditButtonsFrame, text='Up', command=lambda: self.moveTask(moveUp=True))
        self.moveTaskDownButton = ttk.Button(self.taskEditButtonsFrame, text='Down', command=lambda: self.moveTask(moveUp=False))
        self.newTaskButton = ttk.Button(self.taskEditButtonsFrame, text='New', command=self.newTask)
        self.copyTaskButton = ttk.Button(self.taskEditButtonsFrame, text='Copy', command=self.duplicateSelectedTasks)
        self.deleteTaskButton = ttk.Button(self.taskEditButtonsFrame, text='Delete', command=self.deleteTask)

        # tasks table
        self.tasksTableTree = ttk.Treeview(self.tasksFrame, columns=('ID', 'Task name', 'Time'), show='headings')        
        self.tasksTableTree.heading('ID', text='ID')
        self.tasksTableTree.heading('Task name', text='Task name')
        self.tasksTableTree.heading('Time', text='Time')

        # parameter edit
        self.parameterNameLabel = ttk.Label(self.parameterEditFrame, text='Name')
        self.parameterNameEntry = ttk.Entry(self.parameterEditFrame)
        self.parameterValueLabel = ttk.Label(self.parameterEditFrame, text='Value')
        self.parameterValueEntry = ttk.Entry(self.parameterEditFrame)
        self.updateTreeviewParametersButton = ttk.Button(self.parameterEditFrame, text='Update', command=self.updateTreeviewParameters)

        # task parameters
        self.taskParametersTableTree = ttk.Treeview(self.taskParametersFrame, columns=('Parameter name', 'Value'), show='headings')
        self.taskParametersTableTree.heading('Parameter name', text='Parameter name')
        self.taskParametersTableTree.heading('Value', text='Value')
        self.taskFunctionParametersTableTree = ttk.Treeview(self.taskParametersFrame, columns=('Parameter name', 'Value'), show='headings')
        self.taskFunctionParametersTableTree.heading('Parameter name', text='Argument name')
        self.taskFunctionParametersTableTree.heading('Value', text='Value')


        ## position
        # control buttons
        self.newMacroButton.grid(row=0, column=0)
        self.openMacroButton.grid(row=0, column=1)
        self.saveMacroButton.grid(row=0, column=2)
        self.settingsButton.grid(row=0, column=3)

        # run buttons
        self.runButton.grid(row=0, column=0)
        self.killButton.grid(row=0, column=1)

        # utility buttons
        self.cursorPositionButton.grid(row=0, column=0)
        self.variablesButton.grid(row=0, column=1)

        # task edit buttons
        self.moveTaskUpButton.grid(row=0, column=0)
        self.moveTaskDownButton.grid(row=1, column=0)
        self.newTaskButton.grid(row=2, column=0)
        self.copyTaskButton.grid(row=3, column=0)
        self.deleteTaskButton.grid(row=4, column=0)

        # tasks table
        self.tasksTableTree.grid(row=0, column=0)

        # parameter edit
        self.parameterNameLabel.grid(row=0, column=0)
        self.parameterNameEntry.grid(row=0, column=1)
        self.parameterValueLabel.grid(row=0, column=2)
        self.parameterValueEntry.grid(row=0, column=3)
        self.updateTreeviewParametersButton.grid(row=0, column=4)

        # task parameters
        self.taskParametersTableTree.grid(row=0, column=0)
        self.taskFunctionParametersTableTree.grid(row=1, column=0)

        # frames
        # buttons inside first row
        self.controlButtonsFrame.grid(row=0, column=0)
        self.runButtonsFrame.grid(row=0, column=1)
        self.utilityButtonsFrame.grid(row=0, column=2)
        
        # main layout
        self.rowOneButtonsFrame.grid(row=0, column=0, columnspan=3)
        self.tasksFrame.grid(row=1, column=1, rowspan=2)
        self.parameterEditFrame.grid(row=1, column=2)
        self.taskParametersFrame.grid(row=2, column=2)
        self.taskEditButtonsFrame.grid(row=1, column=0, rowspan=2)
        
        self.mainFrame.grid(row=0, column=0)

        ## binds
        self.bind('<ButtonRelease-1>', self.handleMouseClick)

    def _isRunSet(self, state=False):
        '''
        Setter for self.isRun. Handles switching focus styles of self.tasksTableTree.
            state: bool
        '''
        if state:
            self.isRun = state
            self.tasksTableTree['style'] = 'selectionGreen.Treeview'
        else:
            self.isRun = False            
            self.tasksTableTree['style'] = ''
    
    def _clickedTableSet(self, treeview=None, focusedItem=''):
        '''
        Setter for self.clickedTable. Used to verify table of which parameters should be updated.
            treeview -> ttk.Treeview
            focusedItem:str -> item ID returned by .focus()
        '''
        self.clickedTable = treeview, focusedItem

    def _updateTreeviewRow(self, treeview='', rowID='', columnName='', columnValue=''):
        '''
        Sets value of requested cell in treeview
        '''
        treeview.set(rowID, column=columnName, value=columnValue)

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

        if table is not self.tasksTableTree:
            table.insert('', tk.END, values=[''] * len(data[0])) # add empty row in the end
    
    def _handleClickedParameterTreeview(self, treeview):
        '''
        Handles on-click action on parameter treeviews. Gets clicked rowID, updates last clicked treeview and prints focused row data in the Entries.
            treeview: ttk.Treeview
        '''
        _, currentItemID = self._treeviewItemNumber(treeview)                           
        self._clickedTableSet(treeview=treeview, focusedItem=currentItemID)
        parametersDict = treeview.set(currentItemID)
        try:
            self._updateParameterEntries(parameter=parametersDict['Parameter name'], value=parametersDict['Value'])
        except KeyError:
            pass

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
    
    def setEngineVariables(self):
        self.variables = self.macroEngine.getVariables()

    def handleMouseClick(self, event):
        '''
        Handles mouse clicked events. For Treeviews: 1. get clicked item data 2. generate tables or pass data to Entries
        '''
        ## program is not running and macro exists
        if not self.isRun and self.tasksList:
            widget = self.winfo_containing(self.winfo_pointerx(), self.winfo_pointery())
            ## tasks list is clicked 
            if widget == self.tasksTableTree:
                currentItemNumber, _ = self._treeviewItemNumber(self.tasksTableTree)
                self._clickedTableSet(treeview=widget)
                if currentItemNumber is not None:              
                    self.generateParametersTable(currentItemNumber)
            elif widget == self.taskParametersTableTree:
                self._handleClickedParameterTreeview(self.taskParametersTableTree)
            elif widget == self.taskFunctionParametersTableTree:
                self._handleClickedParameterTreeview(self.taskFunctionParametersTableTree)
    
    def openMacroFile(self):
        '''
        Opens macro file and loads variables from the same directory
        '''
        path = os.path.join(os.getcwd(), '')
        macroFile = filedialog.askopenfilename(title='Open macro', initialdir=path, filetypes=(('Macro file','*.json'),))

        ## CREATE PROJECT-FOLDER
        if macroFile:            
            self.filePath = macroFile
            *dirPath, macroName = [val for val in macroFile.split('/')]
            dirPath = '/'.join(item for item in dirPath)
            self.macroEngine.loadVariablesMacro(dirPath, macroName)
            self.setEngineVariables()
            self.generateTasksTable()
    
    def _updateTaskList(self):
        '''
        Updates self.taskist
        '''
        self.tasksList = self.macroEngine.getTaskList() # copy tasklist

    def generateTasksTable(self):
        '''
        Fills tasksTableTree with data
        '''
        self._updateTaskList()
        taskNames = [(i, task.name, '') for i, task in enumerate(self.tasksList)]

        self._clearGenerateTable(self.tasksTableTree, taskNames)
        self.tasksTableChildren = self.tasksTableTree.get_children()

    def runMacro(self):
        '''
        Executes program
        '''
        self._isRunSet(True)
        self.generateTasksTable()
        self.macroEngine.runProgram()
        self._isRunSet(False)

    def generateParametersTable(self, taskID=None):
        '''
        Fills taskParametersTableTree and taskFunctionParametersTableTree with data
        '''
        try:
            task = self.tasksList[taskID]
            parameters = task.taskParametersList()
            arguments = task.functionParametersList()

            self._clearGenerateTable(self.taskParametersTableTree, parameters)
            self._clearGenerateTable(self.taskFunctionParametersTableTree, arguments)
        except IndexError:
            pass
    
    def updateWindow(self, taskID=None, elapsedTime=None):
        '''
        Method called by engine with runtime info about current task
        '''
        # select row 
        currentTaskID = self.tasksTableChildren[taskID]
        self.tasksTableTree.focus(currentTaskID)
        self.tasksTableTree.selection_set(currentTaskID)

        ## display elapsed time
        if elapsedTime:
            self._updateTreeviewRow(treeview=self.tasksTableTree, rowID=currentTaskID, columnName='Time', columnValue=f'{elapsedTime:5f}')
        
        ## refresh window
        self.update()
        self.update_idletasks()
    
    def updateTreeviewParameters(self):
        '''
        Updates task with parameters gained from Entries. 
        1. Get data from Entries
        2. Update Treeviews (update row, clear empty row in the middle, insert empty row)
        3. Convert value to proper type/) to proper type
        '''
        typeDict = {'false': False, 'true':True}
        treeview, rowID = self.clickedTable
        isArgument = treeview == self.taskFunctionParametersTableTree
        parameter = self.parameterNameEntry.get()
        value = self.parameterValueEntry.get()

        ## update tables
        self._updateTreeviewRow(treeview=treeview, rowID=rowID, columnName='Parameter name', columnValue=parameter)
        self._updateTreeviewRow(treeview=treeview, rowID=rowID, columnName='Value', columnValue=value)
        if parameter.lower() == 'name' and not isArgument:            
            self._updateTreeviewRow(treeview=self.tasksTableTree, rowID=rowID, columnName='Task name', columnValue=value)

        ## delete empty row
        if not parameter and not value:
            treeview.delete(rowID)

        ## add empty row as last row, in case that above if-statement cleared last empty row
        lastRow = treeview.get_children()[-1]
        numOfKeys = len(treeview.set(lastRow))
        if treeview.set(lastRow)['Parameter name']:
            treeview.insert('', tk.END, values=[''] * numOfKeys)

        ## update Task instance, update local taskList
        currentItemNumber, _ = self._treeviewItemNumber(self.tasksTableTree)
        if value in self.variables:     
            variableName = value       
            value = self.variables[value]
        else:
            variableName = ''
            ## check if value can be converted to list of ints
            try:
                value = [int(val) for val in value.split(';')]
            except ValueError:
                value = typeDict[value.lower()] if value.lower() in typeDict else value
        self.macroEngine.editTaskParameter(taskID=currentItemNumber, taskParameters=(parameter, value, variableName), isArgument=isArgument)
        self._updateTaskList()

    def deleteTask(self):
        '''
        Delete selected task
        '''
        currentID, _ = self._treeviewItemNumber(self.tasksTableTree)
        self.macroEngine.deleteTask(currentID)
        self.generateTasksTable()
    
    def newTask(self):
        '''
        Creates new task
        '''
        self.macroEngine.newTask()
        self.generateTasksTable()
    
    def moveTask(self, moveUp:bool):
        '''
        Moves selected tasks (rows) in place up or down.
            moveUp: bool -> True = tasks will be moved to the top of the table, False = tasks will be moved to the bottom of the table
        '''
        ## modify self.tasksList in place
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
    
    def duplicateSelectedTasks(self):
        '''
        Duplicates selected tasks in place. New task will be inserted after their original
        '''
        rowIDs = [self.tasksTableChildren.index(row) for row in list(self.tasksTableTree.selection())]
        self.macroEngine.duplicateTasks(rowIDs)
        self.generateTasksTable()

    def getCursorCoords(self):
        '''
        Get cursor coords and pixel color
        '''
        print('You have 5 seconds to move cursor')
        time.sleep(5)
        x, y = pyautogui.position()
        pixelColor = pyautogui.pixel(x, y)
        print(f'coords: ({x}, {y})| RGB:{pixelColor}')

if __name__ == '__main__':
    app = pyMacro()
    app.mainloop()