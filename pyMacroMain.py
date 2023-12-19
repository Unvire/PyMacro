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

        ## frames
        self.mainFrame = ttk.Frame()
        self.rowOneButtonsFrame = ttk.Frame(self.mainFrame)
        self.controlButtonsFrame = ttk.Frame(self.rowOneButtonsFrame)
        self.runButtonsFrame = ttk.Frame(self.rowOneButtonsFrame)
        self.utilityButtonsFrame = ttk.Frame(self.rowOneButtonsFrame)
        self.tasksFrame = ttk.Frame(self.mainFrame)
        self.taskParametersFrame = ttk.Frame(self.mainFrame)
        self.taskEditButtonsFrame = ttk.Frame(self.mainFrame)

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
        self.tasksTableTree = ttk.Treeview(self.tasksFrame, columns=('ID', 'Task name'), show='headings')        
        self.tasksTableTree.heading('ID', text='ID')
        self.tasksTableTree.heading('Task name', text='Task name')

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

        # task parameters
        self.taskParametersTableTree.grid(row=0, column=0)
        self.taskFunctionParametersTableTree.grid(row=1, column=0)

        # frames
        self.controlButtonsFrame.grid(row=0, column=0)
        self.runButtonsFrame.grid(row=0, column=1)
        self.utilityButtonsFrame.grid(row=0, column=2)
        self.rowOneButtonsFrame.grid(row=0, column=0, columnspan=3)

        self.tasksFrame.grid(row=1, column=0)
        self.taskParametersFrame.grid(row=1, column=1)
        self.taskEditButtonsFrame.grid(row=1, column=2)
        
        self.mainFrame.grid(row=0, column=0)
    
    def openMacroFile(self):
        path = os.path.join(os.getcwd(), '')
        macroFile = filedialog.askopenfilename(title='Open macro', initialdir=path, filetypes=(('Macro file','*.json'),))

        ## CREATE PROJECT-FOLDER
        if macroFile:
            self.filePath = macroFile
            self.variablesPath = os.path.join(path, 'variables.json') # variables must be names variables.json and has to be in the same folder as macro file
            self.macroEngine.loadVariablesFile(self.variablesPath)
            self.macroEngine.loadMacroFile(self.filePath)

            self.generateTasksTable()
    
    def generateTasksTable(self):
        self.tasksList = [task for task in self.macroEngine.taskList] # copy tasklist
        taskNames = [(i, task.name) for i, task in enumerate(self.tasksList)]

        ## clear table
        for item in self.tasksTableTree.get_children():
            self.tasksTableTree.delete(item)

        ## add items
        for ID, taskName in taskNames:
            self.tasksTableTree.insert('', tk.END, values=(ID, taskName))

    def runMacro(self):
        self.macroEngine.runProgram()

    def generateparametersTable(self, taskID=None):
        task = self.tasksList[taskID]
        parameters = task.taskParameters()
        arguments = task.functionParameters()

        ## clear table
        for item in self.taskParametersTableTree.get_children():
            self.taskParametersTableTree.delete(item)
        for item in self.taskFunctionParametersTableTree.get_children():
            self.taskFunctionParametersTableTree.delete(item)

        ## add items
        for parameterName, parameterValue in parameters:
            self.taskParametersTableTree.insert('', tk.END, values=(parameterName, parameterValue))
        for argumentName, argumentValue in arguments:
            self.taskFunctionParametersTableTree.insert('', tk.END, values=(argumentName, argumentValue))


        ## display parameters in table
        ## display parameters of parameters in table
        ## generate task on c
        pass

if __name__ == '__main__':
    app = pyMacro()
    app.mainloop()