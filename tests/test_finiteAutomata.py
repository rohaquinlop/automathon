from automathon.finiteAutomata.dfa import *
from automathon.errors.errors import *
import pytest

def test_dfa():
  fa = DFA({'q0', 'q1', 'q2'}, {'0', '1'},  { 'q0' : {'0' : 'q0', '1' : 'q1'},'q1' : {'0' : 'q2', '1' : 'q0'}, 'q2' : {'0' : 'q1', '1' : 'q2'} }, 'q0',
        {'q0'})

  assert fa.isValid() == True

def test_InputError():
  with pytest.raises(InputError) as excinfo:
    
    def f():
      raise InputError('001', 'Is not valid')

    f()
  assert 'Is not valid' in str(excinfo.value)
