import pyautogui

class Cursor:
    def __init__(self):
        pass

    def _processCoords(self, coords=(None, None)) -> (int, int):
        '''
        Method for normalizing coords. They are converted into string, checked if they are numeric and converted into int values. 
        Method returns None for non numeric coordinate, for example '10', 'a' -> 10, None
            coords= x, y sequence
        '''
        x, y = coords
        x = int(x) if str(x).isnumeric() else None
        y = int(y) if str(y).isnumeric() else None
        return x, y

    
    def moveToCoords(self, coords=(None, None), interval=0):
        '''
        Moves cursor to absolute position x, y.
            coords = x, y - sequence of coords. Not numeric coords will be replaced with None, resulting not changing that coordinate
            interval - duration of movement
        '''
        x, y = self._processCoords(coords)
        pyautogui.moveTo(x, y, interval)

    def moveRelative(self, coords=(None, None), interval=0):
        '''
        Moves cursor to x_m + x, y_m + y, where x_m, y_m are current Cursor coordinates.
            coords = x, y - sequence of coords. Not numeric coords will be replaced with None, resulting not changing that coordinate
            interval - duration of movement
        '''
        x, y = self._processCoords(coords)
        pyautogui.move(x, y, interval)

    def dragToCoords(self, coords=(None, None), interval=0, button='left'):
        '''
        Drags (clicks and holds) cursor to x, y
            coords = x, y - sequence of coords. Not numeric coords will be replaced with None, resulting not changing that coordinate
            interval - duration of movement
            button - string name of the button ('left', 'right', 'middle')
        '''
        x, y = self._processCoords(coords)
        pyautogui.dragTo(x, y, interval, button)

    def dragRelative(self, coords=(None, None), interval=0, button='left'):
        '''
        Drags cursor (clicks and holds) x_m + x, y_m + y, where x_m, y_m are current Cursor coordinates
            coords = x, y - sequence of coords. Not numeric coords will be replaced with None, resulting not changing that coordinate
            interval - duration of movement
            button - string name of the button ('left', 'right', 'middle')
        '''
        x, y = self._processCoords(coords)
        pyautogui.drag(x, y, interval, button)

    def click(self, button='left', numOfClicks=1, interval=0.1):
        '''
        Clicks cursor button.
            button - string name of the button ('left', 'right', 'middle')
            numOfClicks - amount of clicked
            interval -  time between clicks
        '''
        pyautogui.click(button=button, clicks=numOfClicks, interval=interval)

    def scroll(self, units=10):
        '''
        Scrolls horizontally by amount of units.
            units - int
        '''
        pyautogui.scroll(units)
    
    def colorUnderCursor(self) -> (int, int, int):
        '''
        Returns color (R, G, B) of pixel pointed by cursor.
        '''
        x, y = pyautogui.position()
        return pyautogui.pixel(x, y)
        

if __name__ == '__main__':
    cursor = Cursor()
    coords1 = '100', 300
    coords2 = 10, 100
    cursor.moveToCoords(coords1)
    cursor.moveRelative(coords2, interval=2)
    cursor.dragToCoords(coords1, button='left')
    cursor.dragRelative(coords2, button='left')
    cursor.click(numOfClicks=2)
    cursor.scroll(20)
    rgb = cursor.colorUnderCursor()
    print(rgb)