import unittest
from automathon import NFA
from automathon.errors.errors import *

class TestNFA(unittest.TestCase):
  fa = NFA(
    Q={'q1', 'q2', 'q3', 'q4'},
    sigma={'0', '1'},
    delta={
      'q1' : {
        '0' : {'q1'},
        '1' : {'q1', 'q2'}
        },
      'q2' : {
        '0' : {'q3'},
        '' : {'q3'}
        },
      'q3' : {
        '1' : {'q4'},
        },
      'q4' : {
        '0' : {'q4'},
        '1' : {'q4'},
        },
      },
      initialState='q1',
      F={'q4'}
  )

  fa_1 = NFA(
    Q={'3', '1', '2', '4', '0'},
    sigma={'', 'AA', 'BB', 'DD', 'CC'},
    delta={
      '0' : {'AA' : {'1'}},
      '1' : {'BB' : {'2'}},
      '2' : {'CC' : {'3'}},
      '3' : {
        '' : {'1'},
        'DD' : {'4'}
        }
      },
    initialState='0',
    F={'4'}
  )
    
  def test_isValid(self):
    self.assertTrue(self.fa.isValid())
  
  def test_accept_str_1(self):
    self.assertTrue(self.fa.accept("000001100001"))
  
  def test_accept_str_2(self):
    self.assertTrue(self.fa.accept("0000011"))
  
  def test_accept_str_3(self):
    self.assertFalse(self.fa.accept("000001"))
  
  def test_remove_epsilon_transitions_1(self):
    no_epsilon_transitions = self.fa_1.remove_epsilon_transitions()
    self.assertTrue(no_epsilon_transitions.isValid())
  
  def test_remove_epsilon_transitions_2(self):
    dfa = self.fa.getDFA()
    self.assertFalse(dfa.accept("000001"))
  
  def test_remove_epsilon_transitions_3(self):
    dfa = self.getDFA()
    self.assertTrue(dfa.accept("0000011"))
  
  def test_nfa_dfa_1(self):
    dfa = self.fa_1.to_dfa()
    self.assertTrue(dfa.isValid())
  
  def test_product(self):
    Q = {'A', 'B'}
    sigma = {'a', 'b'}
    delta = {
      'A' : {
        'a' : {'B'},
        'b' : {'A'}
      },
      'B': {
        'a': {'A'},
        'b': {'B'}
      }
    }
    initialState = 'A'
    F = {'A'}
    
    nfa = NFA(Q, sigma, delta, initialState, F)
    
    Q1 = {'C', 'D'}
    sigma1 = {'a', 'b'}
    delta1 = {
      'C': {
        'a' : {'C'},
        'b' : {'D'}
      },
      'D': {
        'a' : {'D'},
        'b' : {'C'}
      }
    }
    initialState1 = 'C'
    F1 = {'C'}
    
    nfa1 = NFA(Q1, sigma1, delta1, initialState1, F1)
    
    product_result = nfa.product(nfa1)

    self.assertTrue(product_result.isValid())
    self.assertTrue(product_result.accept(""))
    self.assertTrue(product_result.accept("bb"))
    self.assertFalse(product_result.accept("b"))
    self.assertTrue(product_result.accept("bbaa"))
    self.assertFalse(product_result.accept("bbaaa"))
  
  def test_union(self):
    Q = {'A'}
    sigma = {'a'}
    delta = {
      'A' : {
        'a' : {'A'}
      }
    }
    initialState = 'A'
    F = {'A'}
    nfa = NFA(Q, sigma, delta, initialState, F)
    
    Q1 = {'C', 'D', 'E'}
    sigma1 = {'a', 'b'}
    delta1 = {
      'C' : {
        'b' : {'D'},
      },
      'D': {
        'a' : {'E'},
        'b' : {'D'}
      }
    }
    
    initialState1 = 'C'
    F1 = {'E'}
    
    nfa1 = NFA(Q1, sigma1, delta1, initialState1, F1)
    
    union_result = nfa.union(nfa1)

    self.assertTrue(union_result.isValid())
    self.assertTrue(union_result.accept("aaaaaa"))
    self.assertTrue(union_result.accept("bbbbbbbbba"))
    self.assertFalse(union_result.accept("aaaabbbbaaa"))
    self.assertFalse(union_result.accept("aaaaaaaab"))
  
  def test_renumber(self):
    from automathon import DFA
    Q = {'3', '1', '2', '0'}
    sigma = {'', 'A', 'B', 'C'}
    delta = {
      '0': {
        'A': {'1'}
      },
      '1': {
        'B': {'2'},
        '': {'2'}
      },
      '2': {
        'C': {'3'}
      }
    }
    initialState = '0'
    F = {'3'}
    
    automata_1 = NFA(Q, sigma, delta, initialState, F)
    automata_2 = automata_1.removeEpsilonTransitions()
    
    automata_3 = automata_.getDFA()
    automata_4 = automata_3.getNFA()
    automata_4.renumber()

    self.assertTrue(automata_4.isValid())
