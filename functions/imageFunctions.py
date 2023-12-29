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

def screenshot(fileName=None, region=None):
    '''
    Makes a screenshot of requested area and returns it. If fileName is passed then it will save it to a file.
        fileName - str
        region - left, top, width, height - sequence of 4 ints
    '''
    region = _processCoords(coords=region)
    return pyautogui.screenshot(fileName, region)

def locateImage(searchType='any', image=None, region=None, grayscale=False):
    '''
    Checks if image is present in searchedImage. Returns sequence (left, top, width, height) for 'any' or generator that yields (left, top, width, height) for all
        searchType - 'any' - method will stop after first match
                        'all' - method will find all occurances of image
        image - filename/path of image to be searched
        region - left, top, width left - sequence of 4 ints.
        grayscale - convert image to grayscale in order to iprove search time. Can result in false matches
    '''
    locateFunction = {'any':pyautogui.locateOnScreen, 'all':pyautogui.locateAllOnScreen}
    return locateFunction[searchType](image=image, region=region, grayscale=grayscale)
        

    


if __name__ == '__main__':
    screenshot(fileName='test.png', region=(700, 500, 300, 200))
    coords1 = locateImage(searchType='any', image='test.png', region=(0, 0, 1200, 1000))
    print(f'Coords of any matching image: {coords1}')
    coords = locateImage(searchType='all', image='test2.png', region=(0, 0, 1200, 1000))
    print('Coords of all matching images')
    for c in coords:
        print(c)