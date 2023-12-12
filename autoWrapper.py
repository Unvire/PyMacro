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
        pyautogui.moveRel(x, y, interval)

    def dragToCoords(self, coords=(None, None), interval=0, button='left'):
        '''
        Drags (click and hold) cursor to x, y
            coords = x, y - sequence of coords. Not numeric coords will be replaced with None, resulting not changing that coordinate
            interval - duration of movement
            button - string name of the button ('left', 'right', 'middle')
        '''
        x, y = self._processCoords(coords)
        pyautogui.dragTo(x, y, interval, button)

    def dragRelative(self):
        '''
        Drags cursor (clicks and holds) x_m + x, y_m + y, where x_m, y_m are current Cursor coordinates
        '''
        pass

    def click(self):
        '''
        Clicks Cursor button
        '''
        pass

    def scroll(self):
        '''
        Scrolls horizontally or vertically
        '''
        pass

if __name__ == '__main__':
    cursor = Cursor()
    coords1 = '100', 300
    coords2 = 10, 100
    cursor.moveToCoords(coords1)
    cursor.moveRelative(coords2, interval=2)
    cursor.dragToCoords(coords1, button='left')