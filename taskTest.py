import json
from timeit import default_timer as timer
import cursorFunctions

if __name__ == '__main__':
    ## example task file
    macro = {
        0:{                                         # id: int
        'name': 'Move mouse',                       # task name: str
        'enabled': True,                            # enable: bool
        'function': "cursorFunctions.moveToCoords", # function name from module
        'parameters':{                              # parameters dictionary; must be the same as in the calling function, can be less
            'coords': [300, 400],
            'interval': 3}
        },
        1:{                                     
        'name': 'Move mouse again',                   
        'enabled': True,                        
        'function': "cursorFunctions.moveToCoords", 
        'parameters':{                          
            'coords': [500, 600]
            }
        }
    }
    
    ## save and open JSON
    with open('macro.json', 'w') as file:
        json.dump(macro, file, indent=2)
    
    with open('macro.json', 'r') as file:
        macro = json.load(file)

    ## iterate over tasks
    for i in range(2):
        timeStart = timer()
        if macro[str(i)]['enabled']:
            packageName, taskName = macro[str(i)]['function'].split('.')              
            parameters = macro[str(i)]['parameters']
            package = globals()[packageName]        # get package and function from string name
            task = getattr(package, taskName)
            task(**parameters)
        timeEnd = timer()
        print(f'Elapsed time: {timeEnd - timeStart:.3f}')