from automathon.finiteAutomata.dfa import *

def test_dfa():
  fa = DFA({}, {}, dict(), 'q0', {})

  assert fa.getInitialState() == 'q0'