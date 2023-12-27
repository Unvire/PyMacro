import os
import tkinter as tk
from tkinter import ttk, filedialog
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
        self.cursorPositionButton = ttk.Button(self.utilityButtonsFrame, text='Cursor position', command=...)
        self.variablesButton = ttk.Button(self.utilityButtonsFrame, text='Variables', command=...)

        # task edit buttons
        self.moveTaskUpButton = ttk.Button(self.taskEditButtonsFrame, text='Up', command=...)
        self.moveTaskDownButton = ttk.Button(self.taskEditButtonsFrame, text='Down', command=...)
        self.newTaskButton = ttk.Button(self.taskEditButtonsFrame, text='New', command=...)
        self.copyTaskButton = ttk.Button(self.taskEditButtonsFrame, text='Copy', command=...)
        self.deleteTaskButton = ttk.Button(self.taskEditButtonsFrame, text='Delete', command=...)

        # tasks table
        self.tasksTableTree = ttk.Treeview(self.tasksFrame, columns=('ID', 'Task name', 'Time'), show='headings')        
        self.tasksTableTree.heading('ID', text='ID')
        self.tasksTableTree.heading('Task name', text='Task name')
        self.tasksTableTree.heading('Time', text='Time')

        # parameter edit
        self.parameterNameLabel = ttk.Label(self.parameterEditFrame, text='Name')
        self.parameterNameEntry = ttk.Entry(self.parameterEditFrame)
        self.parameterValueLabel = ttk.Label(self.parameterEditFrame, text='Value')
        self.parametervalueEntry = ttk.Entry(self.parameterEditFrame)

        # task parameters
        self.taskParametersTableTree = ttk.Treeview(self.taskParametersFrame, columns=('Parameter name', 'Value'), show='headings')
        self.taskParametersTableTree.heading('Parameter name', text='Parameter name')
        self.taskParametersTableTree.heading('Value', text='Value')
        self.taskFunctionParametersTableTree = ttk.Treeview(self.taskParametersFrame, columns=('Argument name', 'Value'), show='headings')
        self.taskFunctionParametersTableTree.heading('Argument name', text='Argument name')
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
        self.parametervalueEntry.grid(row=0, column=3)

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
        self.tasksFrame.grid(row=1, column=0, rowspan=2)
        self.parameterEditFrame.grid(row=1, column=1)
        self.taskParametersFrame.grid(row=2, column=1)
        self.taskEditButtonsFrame.grid(row=1, column=2, rowspan=2)
        
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
        table.insert('', tk.END, values=[''] * len(row)) # add empty row in the end
    
    def _clearGenerateTable(self, table, data):
        '''
        Calls self._clearTable and self._generateTable - Clears and fills ttk.Treeview with data. 
            table -> ttk.Treeview
            data -> list of tuples that are a row in the table
        '''
        self._clearTable(table)
        self._generateTable(table, data)
    
    def handleMouseClick(self, event):
        '''
        Handles mouse clicked events
        '''
        ## program is not running and macro exists
        if not self.isRun and self.tasksList:
            widget = self.winfo_containing(self.winfo_pointerx(), self.winfo_pointery())
            ## tasks list is clicked 
            if widget == self.tasksTableTree and self.tasksTableChildren:
                currentItemID = self.tasksTableTree.focus()
                try:
                    currentItemNumber = self.tasksTableChildren.index(currentItemID)
                    self.generateParametersTable(currentItemNumber)
                except ValueError:
                    pass
            elif widget == self.taskParametersTableTree:
                print('asd')
            elif widget == self.taskFunctionParametersTableTree:
                print('dsa')
    
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
            self.generateTasksTable()
    
    def generateTasksTable(self):
        '''
        Fills tasksTableTree with data
        '''
        self.tasksList = [task for task in self.macroEngine.taskList] # copy tasklist
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
            self.tasksTableTree.set(currentTaskID, column='Time', value=f'{elapsedTime:5f}')
        
        ## refresh window
        self.update()
        self.update_idletasks()

if __name__ == '__main__':
    app = pyMacro()
    app.mainloop()