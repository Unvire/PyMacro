import json
import cursorWrapper

macro = {1:{
        'name': 'Move mouse',
        'enabled': True,
        'function': cursorWrapper.moveToCoords,
        'parameters':{
            'coords': [300, 400]}
            }
        }

if __name__ == '__main__':
    print(macro[1]['function'])
    print(macro[1]['parameters'])

    macro[1]['function'](**macro[1]['parameters'])