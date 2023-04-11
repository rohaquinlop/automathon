import unittest
from automathon import DFA
from automathon.errors.errors import *

class TestDFA(unittest.TestCase):
  fa = DFA(
    Q={'q0', 'q1', 'q2'},
    sigma={'0', '1'},
    delta={ 'q0' : {'0' : 'q0', '1' : 'q1'},'q1' : {'0' : 'q2', '1' : 'q0'}, 'q2' : {'0' : 'q1', '1' : 'q2'} },
    initialState='q0',
    F={'q0'}
  )

  def test_isValid(self):
    self.assertTrue(self.fa.isValid())
  
  def test_accept_empty(self):
    self.assertTrue(self.fa.accept(""))
  
  def test_accept_str_1(self):
    self.assertTrue(self.fa.accept("001001"))
  
  def test_accept_str_2(self):
    self.assertTrue(self.fa.accept("0101010101010"))
  
  def test_inputError(self):
    with self.assertRaises(InputError) as context:
      self.fa.accept("0010012")
    
    self.assertIn('Is not declared in sigma', context.exception.message)
  
  def test_complement(self):
    notfa = self.fa.complement()
    self.assertFalse(notfa.accept("001001"))
  
  def test_product(self):
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
    
    Q_1 = {'C', 'D'}
    sigma_1 = {'a', 'b'}
    delta_1 = {
      'C': {
        'a': 'C',
        'b': 'D'
      },
      'D': {
        'a': 'D',
        'b': 'C'
      }
    }
    initialState_1 = 'C'
    F_1 = {'C'}
    
    dfa_1 = DFA(Q_1, sigma_1, delta_1, initialState_1, F_1)
    product_result = dfa.product(dfa_1)

    self.assertTrue(product_result.isValid())
    self.assertTrue(product_result.accept(""))
    self.assertTrue(product_result.accept("bb"))
    self.assertFalse(product_result.accept("b"))
  
  def test_product_1(self):
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

    Q_1 = {'R', 'S', 'T', 'U'}
    sigma_1 = {'0', '1'}
    delta_1 = {
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
    initialState_1 = 'R'
    F_1 = {'U'}

    dfa1 = DFA(Q_1, sigma_1, delta_1, initialState_1, F_1)

    product_result = dfa.product(dfa1)

    self.assertTrue(product_result.isValid())
    self.assertTrue(product_result.accept("0001"))
    self.assertFalse(product_result.accept("00010010"))
  
  def test_union(self):
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

    Q_1 = {'R', 'S', 'T', 'U'}
    sigma_1 = {'0', '1'}
    delta_1 = {
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
    initialState_1 = 'R'
    F_1 = {'U'}

    dfa1 = DFA(Q_1, sigma_1, delta_1, initialState_1, F_1)

    union_result = dfa.union(dfa1)

    self.assertTrue(union_result.isValid())
    self.assertTrue(union_result.accept("00010010"))
    self.assertTrue(union_result.accept("0011000"))

if __name__ == '__main__':
  unittest.main()
