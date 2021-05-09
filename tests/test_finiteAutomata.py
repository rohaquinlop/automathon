from automathon import DFA, NFA
from automathon.errors.errors import *
import pytest

def test_dfa_isValid():
  fa = DFA({'q0', 'q1', 'q2'}, {'0', '1'},  { 'q0' : {'0' : 'q0', '1' : 'q1'},'q1' : {'0' : 'q2', '1' : 'q0'}, 'q2' : {'0' : 'q1', '1' : 'q2'} }, 'q0', {'q0'})

  assert fa.isValid() == True

def test_dfa_accept_Epsilon():
  fa = DFA({'q0', 'q1', 'q2'}, {'0', '1'},  { 'q0' : {'0' : 'q0', '1' : 'q1'},'q1' : {'0' : 'q2', '1' : 'q0'}, 'q2' : {'0' : 'q1', '1' : 'q2'} }, 'q0', {'q0'})

  assert fa.accept("") == True ##Empty String

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


def test_complement():
  fa = DFA({'q0', 'q1', 'q2'}, {'0', '1'},  { 'q0' : {'0' : 'q0', '1' : 'q1'},'q1' : {'0' : 'q2', '1' : 'q0'}, 'q2' : {'0' : 'q1', '1' : 'q2'} }, 'q0', {'q0'})

  notfa = fa.complement()

  assert notfa.accept("001001") == False


def test_nfa_isValid():
  Q = {'q1', 'q2', 'q3', 'q4'}
  sigma = {'0', '1'}
  delta = {
            'q1' : {
                    '0' : ['q1'],
                    '1' : ['q1', 'q2']
                   },
            'q2' : {
                    '0' : ['q3'],
                    '' : ['q3']
                   },
            'q3' : {
                    '1' : ['q4'],
                   },
            'q4' : {
                    '0' : ['q4'],
                    '1' : ['q4'],
                   },
          }
  initialState = 'q1'
  F = {'q4'}

  fa = NFA(Q, sigma, delta, initialState, F)

  assert fa.isValid() == True

def test_nfa_accept_input1():
  Q = {'q1', 'q2', 'q3', 'q4'}
  sigma = {'0', '1'}
  delta = {
            'q1' : {
                    '0' : ['q1'],
                    '1' : ['q1', 'q2']
                   },
            'q2' : {
                    '0' : ['q3'],
                    '' : ['q3']
                   },
            'q3' : {
                    '1' : ['q4'],
                   },
            'q4' : {
                    '0' : ['q4'],
                    '1' : ['q4'],
                   },
          }
  initialState = 'q1'
  F = {'q4'}

  fa = NFA(Q, sigma, delta, initialState, F)

  assert fa.accept("000001100001") == True

def test_nfa_accept_input2():
  Q = {'q1', 'q2', 'q3', 'q4'}
  sigma = {'0', '1'}
  delta = {
            'q1' : {
                    '0' : ['q1'],
                    '1' : ['q1', 'q2']
                   },
            'q2' : {
                    '0' : ['q3'],
                    '' : ['q3']
                   },
            'q3' : {
                    '1' : ['q4'],
                   },
            'q4' : {
                    '0' : ['q4'],
                    '1' : ['q4'],
                   },
          }
  initialState = 'q1'
  F = {'q4'}

  fa = NFA(Q, sigma, delta, initialState, F)

  assert fa.accept("0000011") == True ## Make Epsilon Transition


def test_nfa_accept_input3():
  Q = {'q1', 'q2', 'q3', 'q4'}
  sigma = {'0', '1'}
  delta = {
            'q1' : {
                    '0' : ['q1'],
                    '1' : ['q1', 'q2']
                   },
            'q2' : {
                    '0' : ['q3'],
                    '' : ['q3']
                   },
            'q3' : {
                    '1' : ['q4'],
                   },
            'q4' : {
                    '0' : ['q4'],
                    '1' : ['q4'],
                   },
          }
  initialState = 'q1'
  F = {'q4'}

  fa = NFA(Q, sigma, delta, initialState, F)

  assert fa.accept("000001") == False ## Don't make Epsilon Transition

def test_nfa_dfa():
  Q = {'q0', 'q1', 'q2'}
  sigma = {'a', 'b'}
  delta = {
            'q0' : {
                    'a' : ['q0'],
                    'b' : ['q0', 'q1']
                   },
            'q1' : {
                    'b' : ['q2'],
                   }
          }
  initialState = 'q0'
  F = {'q2'}

  fa = NFA(Q, sigma, delta, initialState, F)
  dfa = fa.getDFA()

  assert dfa.isValid() == True

def test_nfa_dfa1():
  Q = {'q1', 'q2', 'q3', 'q4'}
  sigma = {'0', '1'}
  delta = {
            'q1' : {
                    '0' : ['q1'],
                    '1' : ['q1', 'q2']
                    },
            'q2' : {
                    '0' : ['q3'],
                    },
            'q3' : {
                    '1' : ['q4'],
                    },
            'q4' : {
                    '0' : ['q4'],
                    '1' : ['q4'],
                    },
          }
  initialState = 'q1'
  F = {'q4'}

  fa = NFA(Q, sigma, delta, initialState, F)

  tmp = fa.getDFA()

  assert tmp.isValid() == True
