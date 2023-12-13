import json
from timeit import default_timer as timer
import cursorWrapper

if __name__ == '__main__':
    ## example task execution
    macro = {
        0:{                                       # id: int
        'name': 'Move mouse',                     # task name: str
        'enabled': True,                          # enable: bool
        'function': "cursorWrapper.moveToCoords", # function name from module
        'parameters':{                            # parameters dictionary; must be the same as in the calling function, can be less
            'coords': [300, 400],
            'interval': 3}
        },
        1:{                                     
        'name': 'Move mouse',                   
        'enabled': True,                        
        'function': "cursorWrapper.moveToCoords", 
        'parameters':{                          
            'coords': [500, 600]
            }
        }
    }

    with open('macro.json', 'w') as file:
        json.dump(macro, file, indent=2)
        
    for i in range(2):
        timeStart = timer()
        if macro[i]['enabled']:
            package, taskName = macro[i]['function'].split('.')            
            print(package, taskName)
            task = getattr(cursorWrapper, taskName)
            print(task)
            task(**macro[i]['parameters'])
        timeEnd = timer()
        print(f'Elapsed time: {timeEnd - timeStart}')