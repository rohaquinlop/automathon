from automathon import DFA
from automathon.errors.errors import *
import pytest

def test_dfa_isValid():
  fa = DFA({'q0', 'q1', 'q2'}, {'0', '1'},  { 'q0' : {'0' : 'q0', '1' : 'q1'},'q1' : {'0' : 'q2', '1' : 'q0'}, 'q2' : {'0' : 'q1', '1' : 'q2'} }, 'q0', {'q0'})

  assert fa.isValid() == True

def test_dfa_accept_Epsilon():
  fa = DFA({'q0', 'q1', 'q2'}, {'0', '1'},  { 'q0' : {'0' : 'q0', '1' : 'q1'},'q1' : {'0' : 'q2', '1' : 'q0'}, 'q2' : {'0' : 'q1', '1' : 'q2'} }, 'q0', {'q0'})

  assert fa.accept("") == True ##Epsilon

def test_dfa_accept_input1():
  fa = DFA({'q0', 'q1', 'q2'}, {'0', '1'},  { 'q0' : {'0' : 'q0', '1' : 'q1'},'q1' : {'0' : 'q2', '1' : 'q0'}, 'q2' : {'0' : 'q1', '1' : 'q2'} }, 'q0', {'q0'})

  assert fa.accept("001001") == True

def test_dfa_accept_input2():
  fa = DFA({'q0', 'q1', 'q2'}, {'0', '1'},  { 'q0' : {'0' : 'q0', '1' : 'q1'},'q1' : {'0' : 'q2', '1' : 'q0'}, 'q2' : {'0' : 'q1', '1' : 'q2'} }, 'q0', {'q0'})

  with pytest.raises(InputError) as excinfo:
    fa.accept("102")
  
  assert 'Is not declared in sigma' in str(excinfo.value)


def test_dfa_accept_input3():
  ##Test midterm 1 Computability 2021-1
  fa = DFA({'q0', 'q1', 'q2', 'q3'}, {'0', '1'}, { 'q0': {'0': 'q1'}, 'q1': {'1' : 'q2'}, 'q2': {'0' : 'q3'}, 'q3': {'1': 'q2'} }, 'q0', {'q3'})

  assert fa.accept("0101010101010") == True

def test_InputError():
  with pytest.raises(InputError) as excinfo:
    
    def f():
      raise InputError('001', 'Is not valid')

    f()
  assert 'Is not valid' in str(excinfo.value)
