import pyautogui

def _processCoords(coords=(None, None)) -> (int, int):
    '''
    Method for normalizing coords. They are converted into string, checked if they are numeric and converted into int values. 
    Method returns None for non numeric coordinate, for example '10', 'a' -> 10, None
        coords= x, y sequence
    '''
    x, y = coords
    x = int(x) if str(x).isnumeric() else None
    y = int(y) if str(y).isnumeric() else None
    return x, y

def moveToCoords(coords=(None, None), interval=0):
    '''
    Moves cursor to absolute position x, y.
        coords = x, y - sequence of coords. Not numeric coords will be replaced with None, resulting not changing that coordinate
        interval - duration of movement
    '''
    x, y = _processCoords(coords=coords)
    pyautogui.moveTo(x, y, interval)

def moveRelative(coords=(None, None), interval=0):
    '''
    Moves cursor to x_m + x, y_m + y, where x_m, y_m are current Cursor coordinates.
        coords = x, y - sequence of coords. Not numeric coords will be replaced with None, resulting not changing that coordinate
        interval - duration of movement
    '''
    x, y = _processCoords(coords)
    pyautogui.move(x, y, interval)

def dragToCoords(coords=(None, None), interval=0, button='left'):
    '''
    Drags (clicks and holds) cursor to x, y
        coords = x, y - sequence of coords. Not numeric coords will be replaced with None, resulting not changing that coordinate
        interval - duration of movement
        button - string name of the button ('left', 'right', 'middle')
    '''
    x, y = _processCoords(coords)
    pyautogui.dragTo(x, y, interval, button)

def dragRelative(coords=(None, None), interval=0, button='left'):
    '''
    Drags cursor (clicks and holds) x_m + x, y_m + y, where x_m, y_m are current Cursor coordinates
        coords = x, y - sequence of coords. Not numeric coords will be replaced with None, resulting not changing that coordinate
        interval - duration of movement
        button - string name of the button ('left', 'right', 'middle')
    '''
    x, y = _processCoords(coords)
    pyautogui.drag(x, y, interval, button)

def click(button='left', numOfClicks=1, interval=0.1):
    '''
    Clicks cursor button.
        button - string name of the button ('left', 'right', 'middle')
        numOfClicks - amount of clicked
        interval -  time between clicks
    '''
    pyautogui.click(button=button, clicks=numOfClicks, interval=interval)

def scroll(units=10):
    '''
    Scrolls horizontally by amount of units.
        units - int
    '''
    pyautogui.scroll(units)

def colorUnderCursor()-> (int, int, int):
    '''
    Returns color (R, G, B) of pixel pointed by cursor.
    '''
    x, y = pyautogui.position()
    return pyautogui.pixel(x, y)
        

if __name__ == '__main__':
    coords1 = '100', 300
    coords2 = 10, 100
    moveToCoords(coords1)
    moveRelative(coords2, interval=2)
    dragToCoords(coords1, button='left')
    dragRelative(coords2, button='left')
    click(numOfClicks=2)
    scroll(20)
    rgb = colorUnderCursor()
    print(rgb)