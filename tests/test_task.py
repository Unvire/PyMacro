import pytest
import task
import functions.synchroFunctions

@pytest.fixture
def exampleTask():
    exampleTask = task.Task(name='example', 
                            isEnabled=False, 
                            executeFunction=functions.synchroFunctions.nothing, 
                            parameters={'val1':0, 'val2':'test'},
                            isJump=False,
                            variableName='save')
    return exampleTask

def test_initial_value(exampleTask):    
    assert exampleTask.name == 'example'
    assert exampleTask.isEnabled == False
    assert exampleTask.executeFunction is functions.synchroFunctions.nothing
    assert exampleTask.parameters == {'val1':0, 'val2':'test'}
    assert exampleTask.isJump == False
    assert exampleTask.variableName == 'save'

def test_convertToDict(exampleTask):
    expected = {'name':'example', 'isEnabled':False, 'function':'synchroFunctions.nothing', 
                'parameters':{'val1':0, 'val2':'test'}, 'saveResultToVariable':'save'}
    assert exampleTask.convertToDict() == expected

def test_taskParametersList(exampleTask):
    expected = [('name', 'example'), ('isEnabled', False), ('function', 'synchroFunctions.nothing'), ('saveResultToVariable', 'save')]
    assert exampleTask.taskParametersList() == expected

def test_functionParametersList(exampleTask):
    expected = [('val1', '0'), ('val2', 'test')]
    assert exampleTask.functionParametersList() == expected

def test_functionKwargs(exampleTask):
    expected = {'val1':0, 'val2':'test'}
    assert exampleTask.functionKwargs() == expected

def test_updateParameter(exampleTask):
    ## test isJump mofifications 
    exampleTask.updateParameter(isArgument=True, newRecord=('isJump', True))
    assert exampleTask.isJump == True
    exampleTask.updateParameter(isArgument=True, newRecord=('isJump', False))
    assert exampleTask.isJump == False
    
    ## test modification of parameter value and adding new parameter
    exampleTask.updateParameter(isArgument=True, newRecord=('val1', 3))
    exampleTask.updateParameter(isArgument=True, newRecord=('val3', 'New'))
    assert exampleTask.parameters['val3'] == 'New'
    assert exampleTask.parameters['val1'] == 3

    ## test modification of instance variables
    exampleTask.updateParameter(isArgument=False, newRecord=('variableName', 'newSave'))
    assert exampleTask.variableName == 'newSave'

def test_deleteFunctionArgument(exampleTask):
    exampleTask.updateParameter(isArgument=True, newRecord=('val1', 3))
    exampleTask.updateParameter(isArgument=True, newRecord=('val3', 'New'))
    exampleTask.deleteFunctionArgument('val3')
    expected = {'val1':3, 'val2':'test'}
    assert exampleTask.functionKwargs() == expected
