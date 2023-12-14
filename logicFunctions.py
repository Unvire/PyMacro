import re

def equal(val1=None, val2=None):
    return val1 == val2

def notEqual(val1=None, val2=None):
    return not equal(val1, val2)

def greater(val1=None, val2=None):
    return int(val1) > int(val2)

def greaterEqual(val1=None, val2=None):
    return int(val1) >= int(val2)

def less(val1=None, val2=None):
    return int(val1) < int(val2)

def lessEqual(val1=None, val2=None):
    return int(val1) <= int(val2)

def inRange(val, lowerLimit=None, upperLimit=None):
    return int(lowerLimit) <= int(val) <= int(upperLimit)

def notInRange(val, lowerLimit=None, upperLimit=None):
    return not inRange(val, lowerLimit, upperLimit)

def regex(string='', pattern='$'):
    return bool(re.fullmatch(pattern, string))

if __name__ == '__main__':
    print(equal(1, 1), equal(2, 1))
    print(notEqual('a', 'b'), notEqual(2, 1))
    print(greater(1, -1), greater(0, '10'))
    print(greaterEqual(10, 0), greaterEqual(10, 10), greaterEqual(10, 100))
    print(less(1, -1), less(0, '10'))
    print(lessEqual(10, 0), lessEqual(10, 10), lessEqual(10, 100))
    print(inRange(1, 0, 5))
    print(notInRange(-1, 0, 5))
    print(regex(string='aaa', pattern='a*$'), regex(string='aaa', pattern='abc$'))