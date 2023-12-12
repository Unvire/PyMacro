import pyautogui

class Mouse:
    def __init__(self):
        pass
    
    def moveCoords(self):
        '''
        Moves cursor to absolute position x, y
        '''
        pass

    def moveRelative(self):
        '''
        Moves cursor to x_m + x, y_m + y, where x_m, y_m are current mouse coordinates
        '''
        pass

    def dragCoords(self):
        '''
        Drags cursor (clicks and holds) until x, y position is reached
        '''
        pass

    def dragRelative(self):
        '''
        Drags cursor (clicks and holds) x_m + x, y_m + y, where x_m, y_m are current mouse coordinates
        '''
        pass

    def click(self):
        '''
        Clicks mouse button
        '''
        pass

    def scroll(self):
        '''
        Scrolls horizontally or vertically
        '''
        pass