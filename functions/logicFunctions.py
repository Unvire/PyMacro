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
    evaluationFunction = globals()[evaluationFunctionName]
    result = evaluationFunction(*vals)
    return resultTrue if result else resultFalse

def negate(*, val) -> bool:
    return not bool(val)

def equal(*, val1, val2) -> bool:
    return val1 == val2

def notEqual(*, val1, val2) -> bool:
    return not equal(val1=val1, val2=val2)

def greater(*, val1, val2) -> bool:
    return val1 > val2

def greaterEqual(*, val1, val2) -> bool:
    return val1 >= val2

def less(*, val1, val2) -> bool:
    return val1 < val2

def lessEqual(*, val1, val2) -> bool:
    return val1 <= val2

def inRange(*, val, lowerLimit, upperLimit) -> bool:
    return lowerLimit <= val <= upperLimit

def notInRange(*, val, lowerLimit, upperLimit) -> bool:
    return not inRange(val=val, lowerLimit=lowerLimit, upperLimit=upperLimit)

def regex(*, string='', pattern='$') -> bool:
    return bool(re.fullmatch(pattern, string))

if __name__ == '__main__':
    print(negate(val=1))
    print(equal(val1=1, val2=1), equal(val1=2, val2=1))
    print(notEqual(val1='a', val2='b'), notEqual(val1=2, val2=1))
    print(greater(val1=1, val2=-1))
    print(greaterEqual(val1=10, val2=0), greaterEqual(val1=10, val2=10), greaterEqual(val1=10, val2=100))
    print(less(val1=1, val2=-1))
    print(lessEqual(val1=10, val2=0), lessEqual(val1=10, val2=10), lessEqual(val1=10, val2=100))
    print(inRange(val=1, lowerLimit=0, upperLimit=5))
    print(notInRange(val=-1, lowerLimit=0, upperLimit=5))
    print(regex(string='aaa', pattern='a*$'), regex(string='aaa', pattern='abc$'))
    print(checkCondition(evaluationFunctionName='regex', vals=['aaa', 'a*$'], resultTrue=2, resultFalse=-1))