## PyMacro
This program is portable macro editor - step by step user defined instruction list. Used libraries:
- pyautogui -> for handling mouse, keyboard and pixel color in cursor position
- pyperclip -> for handling clipboard
- pyautogui/PIL -> for image matching (search for image in requested area)

## Project description
Each macro project consists of:
- main file (.json) -> files in which step by step instruction list
- variables file (json with not extension) -> file with user defined variables
- Images folder -> contains images for matching

## How to launch?
Option 1. Run:
`pyMacroMain.py`
Option 2. Run:
`pyMacroMain.exe`

## GUI description
First row buttons:
- New Macro -> creates new macro with one 'do nothing' task
- Open Macro -> opens a project. User must choose .json file
- Save Macro -> Saves project. In case of unwanted overwriting (saving a macro inside a project folder wit different name), project will be saved into "New {current date}" folder
- Undo -> allows user to cancel previous up to last 30 modifications. 
- Redo -> reverts action caused by Undo
- Run -> runs program. Run state is indicated by green selection of current running task
- Kill -> kills running program. Shortcut: ctrl+k
- Cursor Position -> initializes a 5 seconds timer. When time reaches zero cursor position (x, y) and pixel color (R, G, B) will be printed on label above table with task list

Tables:
- tasks table -> table in the left column. It contains user defined tasks. Columns are ID, name, run time variable, elapsed time
- task parameter table -> upper table in the right column. It contains common parameters of each task: name, isEnabled, function, saveResultToVariable. Only value can be modified
- function parameters table -> middle table in the right column. It contains parameters of function defined in task parameter table. More information can be found in ... section. Value and parameter name can be modified
- variables table -> bottom table in the right column. It contains user defined variables that will be saved into file. Value and parameter name can be modified

Editing task buttons:
- Up/Down -> changes order of selected task by moving them up or down the table. Select one with left click. Select multiple with ctrl+left click
- New -> inserts new task below selected one. When no task is selected it will be inserted into ID=1
- Copy -> copies selected tasks.Select one with left click. Select multiple with ctrl+left click
- Delete -> deletes one selected task.
- Intend/Uninted -> adds/removes 4 spaces in front of each task name.

Editing task parameters:
- Update -> modifies parameter name of task parameters, function parameters or variables. If name is the same as in the table it will update value. If value in name is different new name:value pair will be added to table
- Delete -> removes selected name:value pair from table

## Data types
Used data types are: bool, int, float, str, list.
List are defined with ';' as separator of items
If it is possible, each str value will be converted into int/float.
Decimal point is '.'

## Variable types
There are 2 types of variables: 
- User defined -> will be saved to file
- run time -> values returned by functions. They will not be saved to file

## Editing task parameters
1. Editing existing parameter
In order to edit task parameter user must firstly select task in the tasks table and then desired parameter, for example name. Then new value must be written into value entry. Lastly user must press Update button to confirm changes
2. Adding new parameter
New parameter can be added by clicking on the blank row below the last one. Then user must write down name:value pair and confirm it with Update button
3. Deleting parameter
Parameter can be deleted by selecting it and pressing delete button

## Common task parameters
Common task parameters are:
- name:str -> name of the task, that will be displayed in tasks table. It is recommended that task names should have unique names. Moreover task names that are labels for conditional jumps must be unique.
- isEnable:bool -> state of the task. If not enabled, the task will not be executed and elapsed time of '-1' will be displayed
- function:str -> executed function written as **{moduleName}.{functionFromModule}**
- saveResultToVariable:str -> if function returns any value, it can be stored as run time variable with given name

## Functions
Functions are defined as package of python files inside "functions" folder. For clarity they will be described as:
`module name: functionName(parameters with expected value types): returned value (if not None) -> description`
*Num* means int or float.
Currently defined functions:
a) **module: synchroFunctions:**
- wait(seconds:num) -> waits for given time in seconds
- nothing() -> does nothing. It is recommended to use this function as jump label
- executeScript(scriptName:str, path:str) -> executes python script given as absolute path folder, scriptName inside that folder
- updateVariable(val:any) -> any -> updates run time variable with val

b) **module: mathFunctions**:
- add(val1:num or str, val2:num or str):num or str -> performs val1 + val2
- substract(val1:num, val2:num):num -> performs val1 - val2
- multiply(val1:num or str, val2:num or str):num or str -> performs val1 * val2
- divide(val1:num, val2:num):num -> performs val1 / val2 (example: 5 / 3 = 1.666666...)
- intDivide(val1:num, val2:num):num -> performs val1 // val2 (example: 5 // 3 = 1)
- pow(base:num, exponent:num):num -> performs base ^ exponent (example: 2 ^ 5 = 32)
- roundNum(roundNum:num, digits:num):num -> round number to requested amount of significant digits
- modulo(val1:num, val2:num):num -> performs val1 % val2

c) **module: logicFunctions:**
- negate(val:any): bool -> performs not bool(val)
- equal(val1:any, val2:any): bool -> performs val1 == val2
- not equal(val1:any, val2:any): bool -> performs val1 != val2
- greater(val1:num, val2:num): bool -> performs val1 > val2
- greaterEqual(val1:num, val2:num): bool -> performs val1 >= val2
- less(val1:num, val2:num): bool -> performs val1 <= val2
- lessEqual(val1:num, val2:num): bool -> performs val1 <= val2
- inRange(val:num, lowerLimit:num, upperLimit:num):bool -> performs lowerLimit <= val <= upperLimit
- notInRange(val:num, lowerLimit:num, upperLimit:num):bool -> performs not(lowerLimit <= val <= upperLimit)
- regex(string:str, pattern:str): bool -> checks for full pattern match using regular expression
- checkCondition(evaluationFunctionName: str, vals:[any, any...], resultTrue:any, resultFalse:any): any -> checks with given logic function described above list of values. Result of functions is either resultTrue or resultFalse - based on the result of evaluating function.

d) **clipboardFunctions:**
- copyTextToClipboard(text:str) -> copies text to clipboard
- copySelectedTextToClipboard() -> copies selected text to clipboard by emulating ctrl+c over selected text
- getFromClipboard(): str -> gets data from clipboard

e) **cursorFunctions:**
- moveToCoords(coords:[int, int], interval:num) -> moves to absolute x, y coords in interval time
- moveRelative(coords:[int, int], interval:num) -> moves x, y units relative to current cursor position in interval time
- dragToCoords(coords:[int, int], interval:num, button:str) -> moves to absolute x, y coordss is reached in interval time and hold button during movement. Button: 'left', 'right', 'middle'
- dragRelative(coords:[int, int], interval:num, button:str) -> moves x, y units relative to current cursor position in interval time and hold button during movement. Button: 'left', 'right', 'middle'
- click(button:str, numOfClicks:int, interval:num) -> clicks a button with interval time between clicks numOfClick times. Button: 'left', 'right', 'middle'
- scroll(units:int) -> scroll by units
- colorUnderCursor(): [int, int, int] -> gets color (R, G, B) under cursor
- getCoords(): [int, int] -> gets coords (x, y) under cursor
- holdButton(button:str) -> presses and holds button. Button: 'left', 'right', 'middle'
- releaseButton(button:str) -> unpresses button. Button: 'left', 'right', 'middle'

f) **keyboardFunctions:**
- writeString(text:str, interval:num) -> writes text by emulating keypresses with interval time between key presses
- press(key:str, numOfPresses:int) -> presses and unpresses key numOfPresses times. List of keys is listed below
- pressAndHold(key:str) -> presses and holds key. Note from pyautogui: "For some reason, this does not seem to cause key repeats like would happen if a keyboard key was held down on a text field."
- unpress(key:str) -> unpresses a key
- keyCombination(keyList:[str, str, ...]) -> presses a key combination and then unpresses. Example keyList: ['ctrl', 'shift', 'esc']
KEYS:['\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace', 'browserback', 'browserfavorites', 'browserforward', 'browserhome', 'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear', 'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete', 'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20', 'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja', 'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail', 'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack', 'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6','num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn', 'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn', 'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator', 'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab', 'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen', 'command', 'option', 'optionleft', 'optionright']

f) **imageFunctions:**
- screenshot(fileName:str, region): image -> Makes a screenshot of requested area and returns it. If fileName is passed then it will save it to a file.
- locateImage(searchType:str, fileName:str, region:None, grayscale:Bool): [int, int, int, int] -> Checks if image passed by fileName is present in region of screen.  Returns sequence (left, top, width, height) for 'any' or generator that yields (left, top, width, height) for all. Grayscale forces images to be grayscaled which improves timing at the expense of accuracy.

## Conditional jump
In order to perform conditional jump user must use *logicFunctions.checkCondition* function and use isJump:True in parameters. In that case resultTrue and resultFalse must be taskNames. Example:
Common parameters:
- name: jump
- function: logicFunctions.checkCondition

Function parameters:
- isJump: True
- evaluationFunctionName: equal
- vals: val1;val2
- resultTrue: Label1
- resultFalse: Label2

If val1 == val2 program will jump to Label1 otherwise to Label2