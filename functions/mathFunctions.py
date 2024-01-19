def add(*, val1, val2):
    return val1 + val2

def substract(*, val1, val2):
    return add(val1=val1, val2=-val2)

def multiply(*, val1, val2):
    return val1 * val2

def divide(*, val1, val2):
    return val1 / val2

def intDivide(*, val1, val2):
    return val1 // val2

def pow(*, base, exponent):
    return base ** exponent

def roundNum(*, val, digits=0):
    return round(val, digits)

def modulo(*, val1, val2):
    return val1 % val2

if __name__ == '__main__':
    print(add(val1=1, val2=3))
    print(substract(val1=1, val2=3))
    print(multiply(val1=2, val2=3))
    print(divide(val1=5, val2=3))
    print(intDivide(val1=5, val2=3))
    print(pow(base=5, exponent=3))
    print(roundNum(val=5.123), roundNum(val=5.123, digits=1))
    print(modulo(val1=7, val2=3))