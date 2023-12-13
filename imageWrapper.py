import pyautogui

class AutoImage:
    def _processCoords(self, coords=(None, None, None, None)) -> (int, int):
        '''
        Method for normalizing coords. They are converted into string, checked if they are numeric and converted into int values. 
        Method returns None for non numeric coordinate, for example '10', 'a', 0, 2 -> 10, None, 0, 2
            coords= top, left, width, height sequence
        '''
        top, left, width, height = coords
        top = int(top) if str(top).isnumeric() else None
        left = int(left) if str(left).isnumeric() else None
        width = int(width) if str(width).isnumeric() else None
        height = int(height) if str(height).isnumeric() else None
        return top, left, width, height

    def screenshot(self, fileName=None, region=None):
        '''
        Makes a screenshot of requested area. If fileName is passed then it will save it to a file.
            fileName - str
            region - left, top, width, height - sequence of 4 ints
        '''
        region = self._processCoords(coords=region)
        return pyautogui.screenshot(fileName, region)
    


if __name__ == '__main__':
    img = AutoImage()
    img.screenshot(fileName='test.png', region=(100, 200, 300, 400))