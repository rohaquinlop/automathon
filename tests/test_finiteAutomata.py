from automathon import DFA, NFA
from automathon.errors.errors import *
import pytest

def test_dfa_accept():
  fa = DFA({'q0', 'q1', 'q2'}, {'0', '1'},  { 'q0' : {'0' : 'q0', '1' : 'q1'},'q1' : {'0' : 'q2', '1' : 'q0'}, 'q2' : {'0' : 'q1', '1' : 'q2'} }, 'q0', {'q0'})

  assert fa.isValid() == True
  assert fa.accept("") == True  ##Empty String
  assert fa.accept("001001") == True
  with pytest.raises(InputError) as excinfo:
    fa.accept("102")

  assert 'Is not declared in sigma' in str(excinfo.value)
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
  assert fa.accept("000001100001") == True
  assert fa.accept("0000011") == True  ## Make Epsilon Transition
  assert fa.accept("000001") == False  ## Don't make Epsilon Transition

def test_remove_epsilon_transitions():
  Q = {'3', '1', '2', '4', '0'}
  sigma = {'', 'AA', 'BB', 'DD', 'CC'}
  delta = {
    '0' : {
           'AA' : ['1']
          },
    '1' : {
           'BB' : ['2']
          },
    '2' : {
           'CC' : ['3']
          },
    '3' : {
           '' : ['1'],
           'DD' : ['4']
          }
  }
  initialState = '0'
  F = {'4'}
  
  automata = NFA(Q, sigma, delta, initialState, F)
  automata2 = automata.removeEpsilonTransitions()
  automata.view('NFA With Epsilon')
  automata2.view('NFA without EpsilonTransitions')


def test_remove_epsilon_transitions1():
  Q = {'0', '1', '2'}
  sigma = {'', 'a', 'b'}
  delta = {
    '0': {
      'a': ['1']
    },
    '1': {
      '': ['2']
    },
    '2': {
      'b': ['2']
    }
  }
  initialState = '0'
  F = {'2'}
  
  automata = NFA(Q, sigma, delta, initialState, F)
  automata2 = automata.removeEpsilonTransitions()
  automata.view('NFA With Epsilon 01')
  automata2.view('NFA without EpsilonTransitions 01')


def test_remove_epsilon_transitions2():
  Q = {'0', '1', '2'}
  sigma = {'', 'a', 'b'}
  delta = {
    '0': {
      'a': ['1']
    },
    '1': {
      '': ['2']
    },
    '2': {
      'b': ['2'],
      '' : ['1']
    }
  }
  initialState = '0'
  F = {'2'}
  
  automata = NFA(Q, sigma, delta, initialState, F)
  automata2 = automata.removeEpsilonTransitions()
  automata.view('NFA With Epsilon 02')
  automata2.view('NFA without EpsilonTransitions 02')

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

def test_nfa_dfa2():
  Q = {'q0', 'q1', 'q2', 'q3'}
  sigma = {'a', 'b'}
  delta = {
    'q0': {
      'a': ['q0', 'q1'],
      'b': ['q0']
    },
    'q1': {
      'a': ['q2'],
    },
    'q2': {
      'a': ['q3'],
    },
    'q3': {
      'a': ['q3'],
      'b': ['q3'],
    },
  }
  initialState = 'q0'
  F = {'q3'}
  
  fa = NFA(Q, sigma, delta, initialState, F)
  
  tmp = fa.getDFA()
  
  tmp.view('dfa')
  fa.view('nfa')
  
  assert tmp.isValid() == True

def test_nfa_removeEpsilon():
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

  nfa = NFA(Q, sigma, delta, initialState, F)
  dfa = nfa.getDFA()

  assert dfa.accept("000001") == False ## Don't make Epsilon Transition
  assert dfa.accept("0000011") == True  ## Make Epsilon Transition

def test_dfa_product():
  Q = {'A', 'B'}
  sigma = {'0', '1'}
  delta = {
            'A' : {
                    '0' : 'A',
                    '1' : 'B'
                   },
            'B' : {
                    '0' : 'B',
                    '1' : 'A'
                   }
          }
  initialState = 'A'
  F = {'B'}
  dfa = DFA(Q, sigma, delta, initialState, F)

  Q1 = {'R', 'S', 'T', 'U'}
  sigma1 = {'0', '1'}
  delta1 = {
            'R' : {
                    '0' : 'S',
                    '1' : 'R'
                  },
            'S' : {
                    '0' : 'T',
                    '1' : 'R'
                  },
            'T' : {
                    '0' : 'U',
                    '1' : 'R'
                  },
            'U' : {
                    '0' : 'U',
                    '1' : 'U'
                  }
          }
  initialState1 = 'R'
  F1 = {'U'}

  dfa1 = DFA(Q1, sigma1, delta1, initialState1, F1)

  dfa2 = dfa.product(dfa1)

  assert dfa2.isValid() == True
  assert dfa2.accept("0001") == True
  assert dfa2.accept("00010010") == False

def test_dfa_product1():
  Q = {'A', 'B'}
  sigma = {'a', 'b'}
  delta = {
    'A': {
      'a': 'B',
      'b': 'A'
    },
    'B': {
      'a': 'A',
      'b': 'B'
    }
  }
  initialState = 'A'
  F = {'A'}
  
  dfa = DFA(Q, sigma, delta, initialState, F)
  
  Q1 = {'C', 'D'}
  sigma1 = {'a', 'b'}
  delta1 = {
    'C': {
      'a': 'C',
      'b': 'D'
    },
    'D': {
      'a': 'D',
      'b': 'C'
    }
  }
  initialState1 = 'C'
  F1 = {'C'}
  
  dfa1 = DFA(Q1, sigma1, delta1, initialState1, F1)
  
  dfa2 = dfa.product(dfa1)

  assert dfa2.isValid() == True
  assert dfa2.accept('') == True
  assert dfa2.accept('bb') == True

  assert dfa2.accept('b') == False

def test_dfa_union():
  Q = {'A', 'B'}
  sigma = {'0', '1'}
  delta = {
            'A' : {
                    '0' : 'A',
                    '1' : 'B'
                   },
            'B' : {
                    '0' : 'B',
                    '1' : 'A'
                   }
          }
  initialState = 'A'
  F = {'B'}
  dfa = DFA(Q, sigma, delta, initialState, F)

  Q1 = {'R', 'S', 'T', 'U'}
  sigma1 = {'0', '1'}
  delta1 = {
            'R' : {
                    '0' : 'S',
                    '1' : 'R'
                  },
            'S' : {
                    '0' : 'T',
                    '1' : 'R'
                  },
            'T' : {
                    '0' : 'U',
                    '1' : 'R'
                  },
            'U' : {
                    '0' : 'U',
                    '1' : 'U'
                  }
          }
  initialState1 = 'R'
  F1 = {'U'}

  dfa1 = DFA(Q1, sigma1, delta1, initialState1, F1)

  dfa2 = dfa.union(dfa1)

  assert dfa2.accept("00010010") == True
  assert dfa2.accept("0011000") == True
  assert dfa.isValid() == True

def test_nfa_union():
  Q = {'A'}
  sigma = {'a'}
  delta = {
    'A' : {
      'a' : ['A']
    }
  }
  initialState = 'A'
  F = {'A'}
  nfa = NFA(Q, sigma, delta, initialState, F)
  
  Q1 = {'C', 'D', 'E'}
  sigma1 = {'a', 'b'}
  delta1 = {
    'C' : {
      'b' : ['D'],
    },
    'D': {
      'a' : ['E'],
      'b' : ['D']
    }
  }
  
  initialState1 = 'C'
  F1 = {'E'}
  
  nfa1 = NFA(Q1, sigma1, delta1, initialState1, F1)
  
  nfa2 = nfa.union(nfa1)
  
  assert nfa2.isValid() == True
  assert nfa2.accept("aaaaaa") == True
  assert nfa2.accept("aaaabbbbaaa") == False
  assert nfa2.accept("bbbbbbbbba") == True
  assert nfa2.accept("aaaaaaaab") == False

def test_nfa_product():
  Q = {'A', 'B'}
  sigma = {'a', 'b'}
  delta = {
    'A' : {
      'a' : ['B'],
      'b' : ['A']
    },
    'B': {
      'a': ['A'],
      'b': ['B']
    }
  }
  initialState = 'A'
  F = {'A'}
  
  nfa = NFA(Q, sigma, delta, initialState, F)
  
  Q1 = {'C', 'D'}
  sigma1 = {'a', 'b'}
  delta1 = {
    'C': {
      'a' : ['C'],
      'b' : ['D']
    },
    'D': {
      'a' : ['D'],
      'b' : ['C']
    }
  }
  initialState1 = 'C'
  F1 = {'C'}
  
  nfa1 = NFA(Q1, sigma1, delta1, initialState1, F1)
  
  nfa2 = nfa.product(nfa1)
  
  assert nfa2.isValid() == True
  assert nfa2.accept('') == True
  assert nfa2.accept('bb') == True
  assert nfa2.accept('b') == False
  assert nfa2.accept('bbaa') == True
  assert nfa2.accept('bbaaa') == False

def test_dfa_nfa():
  Q = {'s1', 's2', 's3'}
  sigma = {'a', 'b'}
  delta = {
    's1': {
      'a' : 's2',
      'b' : 's1'
    },
    's2': {
      'a' : 's2',
      'b' : 's3'
    },
    's3': {
      'a' : 's2',
      'b' : 's1'
    }
  }
  initialState = 's1'
  F = {'s3'}
  
  dfa = DFA(Q, sigma, delta, initialState, F)
  nfa = dfa.getNFA()
  
  assert dfa.isValid() == True
  assert nfa.isValid() == True
  assert dfa.accept('') == nfa.accept('')
  assert dfa.accept('aaab') == nfa.accept('aaab')
  assert dfa.accept('aaaba') == nfa.accept('aaaba')
  assert dfa.accept('aaabb') == nfa.accept('aaabb')

def test_nfa_minimization():
  Q = {'3', '1', '2', '0'}
  sigma = {'', 'A', 'B', 'C'}
  delta = {
    '0': {
      'A': ['1']
    },
    '1': {
      'B': ['2'],
      '' : ['2']
    },
    '2': {
      'C': ['3']
    }
  }
  initialState = '0'
  F = {'3'}
  
  automata = NFA(Q, sigma, delta, initialState, F)
  automata2 = automata.removeEpsilonTransitions()
  
  automata3 = automata.getDFA()
  automata4 = automata3.getNFA()
  automata5 = automata.minimize()
  
  automata2.view('minimize - NFA without EpsilonTransitions')
  automata3.view('minimize - DFA from NFA')
  automata4.view('minimize - NFA from DFA')
  automata5.view('minimize - result of minimization')
