import pyautogui

class Keyboard():
    def writeString(self, text, interval=0):
        '''
        Converts given text to keypresses, which result in emulating of writing.
            text - str
            interval - float -> delay between characters
        '''
        pyautogui.write(text, interval)

    def pressAndUnpressKey(self):
        '''
        '''
        pass

    def pressKey(self):
        '''
        '''
        pass
    
    def unpressKey(self):
        '''
        '''
        pass

    def pressKeyCombination(self):
        '''
        '''
        pass

if __name__ == '__main__':
    kb = Keyboard()
    kb.writeString('Test\n')