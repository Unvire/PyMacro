import pytest, collections
import macroEngine
import functions.logicFunctions, functions.cursorFunctions

@pytest.fixture
def initEngine():
    return macroEngine.MacroEngine()

def test_initState(initEngine):
    item = [], {}
    queue = collections.deque()
    queue.append(item)    
    assert initEngine.undoStack == queue

def test_dynamicImport(initEngine):
    expected = functions.logicFunctions.equal
    assert initEngine._dynamicImportModule("logicFunctions.equal") is expected

def test_createTask(initEngine):
    taskDict = {
                "name": "Move mouse",
                "isEnabled": True,
                "function": "cursorFunctions.moveToCoords",
                "parameters": {
                    "coords": "position1",
                    "interval": 3
                },
                "saveResultToVariable": ""}
    taskInstance = initEngine._createTask(taskDict)
    assert taskInstance.name == "Move mouse"
    assert taskInstance.isEnabled == True
    assert taskInstance.executeFunction is functions.cursorFunctions.moveToCoords
    assert taskInstance.parameters == {'coords': 'position1', 'interval':3}
    assert taskInstance.variableName == ''

def test_intend(initEngine):
    initEngine.newTask(0)
    initEngine.intendTask(0)
    assert initEngine.taskList[0].name == '    New task'
    initEngine.intendTask(0)
    assert initEngine.taskList[0].name == '        New task'

def test_unintend(initEngine):
    initEngine.newTask(0)
    initEngine.intendTask(0); initEngine.intendTask(0)
    initEngine.unintendTask(0)
    assert initEngine.taskList[0].name == '    New task'
    initEngine.unintendTask(0)
    assert initEngine.taskList[0].name == 'New task'
    initEngine.unintendTask(0)
    assert initEngine.taskList[0].name == 'New task'

@pytest.mark.parametrize(('s, expected'), [('a', 'a'), ('  abc   ', 'abc'), ('0.0900axzc', '0.0900axzc'), 
                                             ('0.123', 0.123), ('0', 0), ('1000', 1000), ('-32', -32), ('-89.1', -89.1)])
def test_str2Num(initEngine, s, expected):
    assert initEngine.strToNum(s) == expected

@pytest.mark.parametrize(('s, expected'), [('a ; 12; 32.1; -56;-a', ['a', 12, 32.1, -56, '-a'])])
def test_strToNumList(initEngine, s, expected):
    assert initEngine.strToNumList(s) == expected

def test_calculateKwargs(initEngine):    
    initEngine.variables = {'varText': 'test', 'varNum': 12, 'varList':[30, 712, 'a']}
    testKwargs = {'val1': 'varText', 'val2':13, 'val3':'varNum', 'val4':'varList', 'val5':'-varNum', 'val6':['varText', '-varNum']}
    expected = {'val1': 'test', 'val2':13, 'val3':12, 'val4':[30, 712, 'a'], 'val5':-12, 'val6':['test', -12]}
    assert initEngine.calculateKwargs(testKwargs) == expected
    testKwargs['val7'] = 'newEntry'
    assert testKwargs != expected

def test_findGroups(initEngine):
    expected = [[0, 4], [12, 2], [50, 2], [69, 4], [1241, 1]]
    assert initEngine.findGroups([1, 2, 3, 0, 12, 13, 1241, 50, 51, 69, 70, 71, 72]) == expected

def test_swapTasks(initEngine):
    initEngine.setTaskList([i for i in range(10)])
    group1 = [[0, 3], [7, 1]]
    group2 = [[3, 3], [8, 2]]
    
    ## check out of bounds
    assert initEngine.swapTasks(group1, True) == True
    assert initEngine.swapTasks(group2, False) == True

    ## check moving up
    assert initEngine.swapTasks(group2, True) == False
    movedUpList = initEngine.getTaskList()
    assert movedUpList == [0, 1, 3, 4, 5, 2, 6, 8, 9, 7]

    ## check moving down
    initEngine.setTaskList([i for i in range(10)])
    assert initEngine.swapTasks(group1, False) == False
    movedDownList = initEngine.getTaskList()
    assert movedDownList == [3, 0, 1, 2, 4, 5, 6, 8, 7, 9]

