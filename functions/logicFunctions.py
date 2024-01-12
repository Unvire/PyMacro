import re

def checkCondition(evaluationFunctionName='equal', vals=[1, 2], resultTrue='2', resultFalse='0'):
    '''
    If statement that can be called as task function. Returns either resultTrue or resultFalse - based on the evaulation.
        evalationFunctionName: str -> name of the evaulation function declared in this script. Evaulation functions with arguments are listed below:
            negate(val) -> not bool(val)
            equal(val1, val2) -> val1 == val2
            notEqual(val1, val2) -> val1 != val2
            greater(val1, val2) -> val1 > val2
            greaterEqual(val1, val2)  -> val1 >= val2
            less(val1, val2)  -> val1 < val2
            lessEqual(val1, val2) -> val1 <= val2
            inRange(val, lowerLimit, upperLimit) -> lowerLimit <= val <=upperLimit
            notInRange(val, lowerLimit, upperLimit) -> not(lowerLimit <= val <=upperLimit)
            regex(string='', pattern='$') 
        vals:list -> list of arguments for evaluation function. Order is important
        resultTrue, resultFalse - retured values based on the evaluation
    '''
    evalationFunction = globals()[evaluationFunctionName]
    result = evalationFunction(*vals)
    return resultTrue if result else resultFalse

def negate(val) -> bool:
    return not bool(val)

def equal(val1, val2) -> bool:
    return val1 == val2

def notEqual(val1, val2) -> bool:
    return not equal(val1, val2)

def greater(val1, val2) -> bool:
    return int(val1) > int(val2)

def greaterEqual(val1, val2) -> bool:
    return int(val1) >= int(val2)

def less(val1, val2) -> bool:
    return int(val1) < int(val2)

def lessEqual(val1, val2) -> bool:
    return int(val1) <= int(val2)

def inRange(val, lowerLimit, upperLimit) -> bool:
    return int(lowerLimit) <= int(val) <= int(upperLimit)

def notInRange(val, lowerLimit, upperLimit) -> bool:
    return not inRange(val, lowerLimit, upperLimit)

def regex(string='', pattern='$') -> bool:
    return bool(re.fullmatch(pattern, string))

if __name__ == '__main__':
    print(negate(1))
    print(equal(1, 1), equal(2, 1))
    print(notEqual('a', 'b'), notEqual(2, 1))
    print(greater(1, -1), greater(0, '10'))
    print(greaterEqual(10, 0), greaterEqual(10, 10), greaterEqual(10, 100))
    print(less(1, -1), less(0, '10'))
    print(lessEqual(10, 0), lessEqual(10, 10), lessEqual(10, 100))
    print(inRange(1, 0, 5))
    print(notInRange(-1, 0, 5))
    print(regex(string='aaa', pattern='a*$'), regex(string='aaa', pattern='abc$'))
    print(checkCondition(evalationFunctionName='regex', vals=['aaa', 'a*$'], resultTrue=2, resultFalse=-1))