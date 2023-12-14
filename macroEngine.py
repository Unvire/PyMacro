import json
from timeit import default_timer as timer

import keyboardFunctions
import cursorFunctions
import imageFunctions

class Task:
    pass

class MacroEngine:
    def __init__(self):
        self.taskList = []

    def _createTasks(self):
        pass

    def loadJSON(self, filePath):
        with open(filePath, 'r') as file:
            taskDict = json.load(file)
        print(taskDict)

    def saveJSON(self):
        pass

    def executeTask(self):
        pass

if __name__ == '__main__':
    engine = MacroEngine()
    engine.loadJSON('macro.json')