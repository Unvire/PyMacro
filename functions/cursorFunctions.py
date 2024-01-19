import pyautogui

def _processCoords(coords=(None, None)) -> (int, int):
    '''
    Method for normalizing coords. They are converted into string, checked if they are numeric and converted into int values. 
    Method returns None for non numeric coordinate, for example '10', 'a' -> 10, None
        coords= x, y sequence
    '''
    x, y = coords
    try:
        x = int(x)
    except ValueError:
        x = None
    try:
        y = int(y)
    except ValueError:
        y = None
    return x, y

def moveToCoords(*, coords=(None, None), interval=0):
    '''
    Moves cursor to absolute position x, y.
        coords = x, y - sequence of coords. Not numeric coords will be replaced with None, resulting not changing that coordinate
        interval - duration of movement
    '''
    x, y = _processCoords(coords=coords)
    pyautogui.moveTo(x, y, int(interval))

def moveRelative(*, coords=(None, None), interval=0):
    '''
    Moves cursor to x_m + x, y_m + y, where x_m, y_m are current Cursor coordinates.
        coords = x, y - sequence of coords. Not numeric coords will be replaced with None, resulting not changing that coordinate
        interval - duration of movement
    '''
    x, y = _processCoords(coords)
    pyautogui.move(x, y, int(interval))

def dragToCoords(*, coords=(None, None), interval=0, button='left'):
    '''
    Drags (clicks and holds) cursor to x, y
        coords = x, y - sequence of coords. Not numeric coords will be replaced with None, resulting not changing that coordinate
        interval - duration of movement
        button - string name of the button ('left', 'right', 'middle')
    '''
    x, y = _processCoords(coords)
    pyautogui.dragTo(x, y, int(interval), button)

def dragRelative(*, coords=(None, None), interval=0, button='left'):
    '''
    Drags cursor (clicks and holds) x_m + x, y_m + y, where x_m, y_m are current Cursor coordinates
        coords = x, y - sequence of coords. Not numeric coords will be replaced with None, resulting not changing that coordinate
        interval - duration of movement
        button - string name of the button ('left', 'right', 'middle')
    '''
    x, y = _processCoords(coords)
    pyautogui.drag(x, y, int(interval), button)

def click(*, button='left', numOfClicks=1, interval=0.1):
    '''
    Clicks cursor button.
        button - string name of the button ('left', 'right', 'middle')
        numOfClicks - amount of clicked
        interval -  time between clicks
    '''
    pyautogui.click(button=button, clicks=numOfClicks, interval=int(interval))

def scroll(*, units=10):
    '''
    Scrolls horizontally by amount of units.
        units - int
    '''
    pyautogui.scroll(int(units))

def colorUnderCursor(*, coords:(int, int)=()) -> (int, int, int):
    '''
    Returns color (R, G, B) of pixel pointed by cursor.
        coords=(x, y) -> optional tuple of coords that specify pixel. If no value is passed then cursor coords will be used
    '''
    if coords:
        x, y = _processCoords(coords)
    else:
        x, y = getCoords()
    return pyautogui.pixel(x, y)

def getCoords() -> (int, int):
    '''
    Returns coords (x, y) of pixel pointed by cursor.
    '''
    x, y = pyautogui.position()
    return x, y

def holdButton(*, button='left'):
    '''
    Holds down a mouse button
    '''
    pyautogui.mouseDown(button=button)

def releaseButton(*, button='left'):
    '''
    Releases a mouse button
    '''
    pyautogui.mouseUp(button=button)

if __name__ == '__main__':
    coords1 = '100', 300
    coords2 = 10, 100    
    print(getCoords())
    moveToCoords(coords=coords1)
    moveRelative(coords=coords2, interval=2)
    dragToCoords(coords=coords1, button='left')
    dragRelative(coords=coords2, button='left')
    click(numOfClicks=2)
    scroll(units=20)
    rgb = colorUnderCursor()
    print(rgb)
    print(colorUnderCursor(coords=(-219, 548)))