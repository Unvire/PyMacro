import pyautogui
import pyperclip

def copyTextToClipboard(*, text=''):
    pyperclip.copy(text)

def copySelectedTextToClipboard():
    ''' Copies selected text by emulating ctrl-c hotkey '''
    pyautogui.hotkey(['ctrl', 'c'])

def getFromClipboard() -> str:
    text = pyperclip.paste()
    return text

if __name__ == '__main__':
    copySelectedTextToClipboard()
    print(getFromClipboard())
    copyTextToClipboard(text='Hello world')    
    print(getFromClipboard())