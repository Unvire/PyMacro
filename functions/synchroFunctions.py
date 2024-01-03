import time

def wait(seconds=1):
    time.sleep(int(seconds))

def nothing():
    pass

if __name__ == '__main__':
    wait(3)
    nothing()