def add(val1, val2):
    return val1 + val2

def substract(val1, val2):
    return add(val1, -val2)

def multiply(val1, val2):
    return val1 * val2

def divide(val1, val2):
    return val1 / val2

def intDivide(val1, val2):
    return val1 // val2

def pow(base, exponent):
    return base ** exponent

def roundNum(val, digits=0):
    return round(val, digits)

def modulo(val1, val2):
    return val1 % val2

if __name__ == '__main__':
    print(add(1, 3))
    print(substract(1, 3))
    print(multiply(2, 3))
    print(divide(5, 3))
    print(intDivide(5, 3))
    print(pow(5, 3))
    print(roundNum(5.123), roundNum(5.123, 1))