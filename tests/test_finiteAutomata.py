from pythomata.finiteAutomata.dfa import *

def test_dfa():
  fa = DFA(initialState='q0')

  assert fa.getInitialState() == 'q0'