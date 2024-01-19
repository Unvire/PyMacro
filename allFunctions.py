import importlib
import os
import inspect

def getFunctionNames():
    importedModules = {}
    modules = ['.' + fileName[:-3] for fileName in os.listdir(os.path.join(os.getcwd(), 'functions')) if fileName[1] != '_']
    functionsList = []

    for module in modules:
        importedModules[module] = importlib.import_module(module, package='functions')
        moduleFunctions = inspect.getmembers(importedModules[module], inspect.isfunction)
        for fun, _ in moduleFunctions:
            functionsList.append(f'{module[1:]}.{fun}')
    
    parameterNames = ['val', 'vals', 'val1', 'val2', 'valType', 'seconds', 'scriptName', 'path', 'digits', 'evaluationFunctionName', 
                      'resultTrue', 'resultFalse', 'isJump', 'lowerLimit', 'upperLimit', 'string', 'pattern', 'text', 'interval',
                      'numOfPresses', 'key', 'keysList', 'fileName', 'region', 'searchType', 'grayscale', 'coords', 'button', 'numOfClicks',
                      'units'
                      ]
    return functionsList + parameterNames

if __name__ == '__main__':
    print(getFunctionNames())


