import time

def wait(seconds=1):
    time.sleep(int(seconds))

def nothing():
    pass

def initVariable(*, val, valType='int'):
    valType = valType.lower()
    typeDict = {'int': int, 'float':float, 'str':str, 'bool':bool}
    if valType == 'bool':
        val = val.lower()
        return val == 'true'
    return typeDict[valType](val)

if __name__ == '__main__':
    wait(3)
    nothing()
    print(initVariable(val='3', valType='float'))