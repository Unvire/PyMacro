import pyautogui

class AutoImage:

    def screenshot(self, fileName=None, region=None):
        '''
        Makes a screenshot of requested area. If fileName is passed then it will save it to a file.
            fileName - str
            region - left, top, width, height - sequence of 4 ints
        '''
        return pyautogui.screenshot(fileName, region)

if __name__ == '__main__':
    img = AutoImage()
    img.screenshot(fileName='test.png', region=(100, 200, 300, 400))