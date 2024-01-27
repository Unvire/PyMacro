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

def test_calculateKwargs():
    pass

def test_findGroups():
    pass

def test_swapTasks():
    pass

