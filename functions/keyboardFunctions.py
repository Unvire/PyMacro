import pyautogui

'''
KEYS:
['\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(',
')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
'8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
'browserback', 'browserfavorites', 'browserforward', 'browserhome',
'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
'command', 'option', 'optionleft', 'optionright']
'''

def writeString(*, text='', interval=0):
    '''
    Converts given text to keypresses, which result in emulating of writing.
        text - str
        interval - float -> delay between characters
    '''
    pyautogui.write(str(text), int(interval))

def press(*, key='', numOfPresses=1):
    '''
    Presses and unpresses key
    '''
    pyautogui.press(key, presses=int(numOfPresses))

def pressAndHold(*, key=''):
    '''
    Presses and holds key. DO NOT FORGET TO UNPRESS IT WITH unpress(key) method.
    NOTE: For some reason, this does not seem to cause key repeats like would
    happen if a keyboard key was held down on a text field.
    '''
    pyautogui.keyDown(key)

def unpress(*, key=''):
    '''
    Unpresses key
    '''
    pyautogui.keyUp(key)

def keyCombination(*, keysList=[]):
    '''
    Presses combination of keys
        keysList - sequence of keys, for example ['ctrl', 'shift', 'esc']
    '''
    pyautogui.hotkey(keysList)

if __name__ == '__main__':
    writeString(text='Test')
    press(key='a', numOfPresses=10)
    pressAndHold(key='b')
    unpress(key='b')
    keyCombination(keysList=['ctrl', 'shift', 'esc'])