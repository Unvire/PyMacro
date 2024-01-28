import pyautogui


def _processCoords(coords=(None, None, None, None)) -> (int, int, int, int):
    '''
    Method for normalizing coords. They are converted into string, checked if they are numeric and converted into int values. 
    Method returns None for non numeric coordinate, for example '10', 'a', 0, 2 -> 10, None, 0, 2
        coords= top, left, width, height sequence
    '''
    top, left, width, height = coords
    try:
        top = int(top)
    except ValueError:
        top = None
    try:
        left = int(left)
    except ValueError:
        left = None
    width = int(width) if str(width).isnumeric() else None
    height = int(height) if str(height).isnumeric() else None
    return top, left, width, height

def screenshot(*, fileName=None, region=None):
    '''
    Makes a screenshot of requested area.
        fileName: str - path to where to save screenshot
        region - left, top, width, height - sequence of 4 ints
    '''
    region = _processCoords(coords=region)
    pyautogui.screenshot(fileName, region)

def locateImage(fileName=None, region=None, grayscale=False):
    '''
    Checks if image is present in searchedImage. Returns sequence left, top of first found image
        fileName - filename/path of image to be searched
        region - left, top, width left - sequence of 4 ints.
        grayscale - convert image to grayscale in order to improve search time. Can result in false matches
    '''    
    result = pyautogui.locateOnScreen(image=fileName, region=region, grayscale=grayscale)
    if result:
        left, top, *_ = result
    else:
        left, top = 'None', 'None'
    return left, top

if __name__ == '__main__':    
    from time import sleep
    screenshot(fileName='test.png', region=(700, 500, 300, 200))
    coords1 = locateImage(fileName='test.png', region=(0, 0, 1200, 1000))
    print(f'Coords of any matching image: {coords1}')
    sleep(5)
    coords2 = locateImage(fileName='test.png', region=(0, 0, 1200, 1000), grayscale=True)
    print(f'Coords of any matching image: {coords2}')